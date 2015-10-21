from flask import Flask, render_template, request, redirect, url_for, flash
from flask import jsonify, session as login_session, make_response
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Author, Book, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from oauth2client import client, crypt
from functools import wraps
import json, random, string, httplib2, requests

# Flask Setup
app = Flask(__name__)

# Client ID for Google Oauth
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog"

# SQL setup
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Generate anti-request-forgery state token, render login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Request token, verify, login, and store user. 
@app.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    # verify state token to stop cross site forgery
    if request.args.get('state') != login_session['state']:
       response = make_response(json.dumps('Invalid state parameter.'), 401)
       response.headers[Content-Type] = 'application/json'
       return response
    code = request.data
    
    # Exchange token for credentials 
    try:
        flow = flow_from_clientsecrets('client_secrets.json',
                                       scope='openid email', 
                                       redirect_uri='postmessage')
        credentials = flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify credentials
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % credentials.access_token)
    h = httplib2.Http()
    idinfo = json.loads(h.request(url, 'GET')[1])
    
    # Check for errors, abort and report errors
    if idinfo.get('error') is not None:
        response = make_response(json.dumps(idinfo.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    if idinfo['issued_to'] != CLIENT_ID:
        raise crypt.AppIdentityError("Token's client ID does not match app's")
    if idinfo['user_id'] != credentials.id_token['sub']:
        raise crypt.AppIdentityError("Wrong user.")

    # Check stored credentials    
    gplus_id = idinfo['user_id']
    stored_credentials = login_session.get('credentials')
    stored_id = login_session.get('gplus_id')
    
    # Compare stored and current credentials, check if user is already logged in
    if stored_credentials is not None and gplus_id == stored_id:
        response = make_response(
            json.dumps('Current user is already connected.'),200)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Store credentials in session
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Request user information
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # Store information in session
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['provider'] = 'google'

    # Add user to database if not already added
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    
    # Update page with user information
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'], 
          "alert-success")
    return output

# Add new user to database
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

# Get user information from database
def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

# Get user ID by email from database, return none if user is no in database
def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None
        
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            return redirect(url_for('showLogin'))
        return func(*args, **kwargs)
    return decorated_function
    

# Clear ALL Flask session information, can only be accesed directly
@app.route('/clearSession')
def clearSession():
    login_session.clear()
    return "Session cleared"

# Log user out
@app.route('/gdisconnect')
def gdisconnect():
    # Check if user is connected
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    
    # Delete session information if successful and redirect, display errors
    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        
        flash('Successfully logged out', "alert-success")
        return redirect(url_for('showAuthors'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# JSON author List endpoint
@app.route('/author/JSON')
def authorListJSON():
    authors = session.query(Author).all()
    return jsonify(authors=[author.serialize for author in authors])

# JSON book list endpoint
@app.route('/author/<int:author_id>/books/JSON')
def bookListJSON(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    books = session.query(Book).filter_by(
        author_id=author_id).all()
    return jsonify(books=[book.serialize for book in books])

# JSON book information endpoint
@app.route('/author/<int:author_id>/books/<int:book_id>/JSON')
def bookJSON(author_id, book_id):
    book = session.query(Book).filter_by(id=book_id).one()
    return jsonify(book=book.serialize)

# Main page, List of authors
@app.route('/')
@app.route('/author/')
def showAuthors():
    authors = session.query(Author).order_by(asc(Author.name))
    if 'username' not in login_session:
        return render_template('publicAuthors.html', authors = authors)
    else:
        return render_template('authors.html', authors = authors)

@app.route('/author/new/', methods=['GET', 'POST'])
@login_required
def newAuthor():
    if request.method == 'POST':
        newAuthor = Author(name=request.form['name'],
                           user_id=login_session['user_id'])
        session.add(newAuthor)
        session.commit()
        flash('New Author %s Successfully Added' % newAuthor.name, 
              "alert-success")
        return redirect(url_for('showAuthors'))
    else:
        return render_template('newAuthor.html')

# Page for editing author
@app.route('/author/<int:author_id>/edit', methods=['GET', 'POST'])
@login_required
def editAuthor(author_id):
    editedAuthor = session.query(Author).filter_by(id=author_id).one()
    if editedAuthor.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this author. Please create your own author in order to edit.');history.back();}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedAuthor.name = request.form['name']
            flash('Author Successfully Edited: %s' % editedAuthor.name, 
                  "alert-success")
            return redirect(url_for('showAuthors'))
    else:
        return render_template('editAuthor.html', author=editedAuthor)

# Page for deleting author
@app.route('/author/<int:author_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteAuthor(author_id):
    authorDelete = session.query(
        Author).filter_by(id=author_id).one()
    if authorDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this author. Please create your own author in order to delete.');history.back();}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(authorDelete)
        session.commit()
        flash('Author Successfully Removed: %s' % authorDelete.name, 
              "alert-success")
        return redirect(url_for('showAuthors', author_id=author_id))
    else:
        return render_template('deleteAuthor.html', author=authorDelete)

# List of books by author
@app.route('/author/<int:author_id>/')
@app.route('/author/<int:author_id>/books/')
def showBooks(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    creator = getUserInfo(author.user_id)
    books = session.query(Book).filter_by(author_id=author_id).all()
    if 'username' not in login_session or creator.id != login_session['user_id']:
        return render_template('publicBooks.html', 
                               books=books, author=author, creator=creator)
    return render_template('books.html', books=books, author=author)

# Page to add new book by author
@app.route('/author/<int:author_id>/books/new', methods=['GET', 'POST'])
@login_required
def newBook(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    if author.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to add to this author. Please create your own author in order to add books.');history.back();}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newBook = Book(name=request.form['name'],
                       picture=request.form['picture'],
                       description=request.form['description'],
                       price=request.form['price'],
                       author_id=author_id,
                       user_id=author.user_id)
        session.add(newBook)
        session.commit()
        flash('New Book %s Successfully Added' % newBook.name, "alert-success")
        return redirect(url_for('showBooks', author_id=author_id))
    else:
        return render_template('newBook.html', author=author)

# Page to delete book by author
@app.route('/author/<int:author_id>/books/<int:book_id>/delete',
           methods=['GET', 'POST'])
@login_required
def deleteBook(author_id, book_id):
    authorDelete = session.query(Author).filter_by(id=author_id).one()
    bookDelete = session.query(Book).filter_by(id=book_id).one()
    if authorDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete from this author. Please create your own author in order to delete books.');history.back();}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(bookDelete)
        session.commit()
        flash('Book Successfully Removed: %s' % bookDelete.name, 
              "alert-success")
        return redirect(url_for('showBooks', author_id=author_id))
    else:
        return render_template('deleteBook.html', author=authorDelete,
                               book=bookDelete)

# Page to edit book by author
@app.route('/author/<int:author_id>/books/<int:book_id>/edit',
           methods=['GET', 'POST'])
@login_required
def editBook(author_id, book_id):
    editedAuthor = session.query(Author).filter_by(id=author_id).one()
    editedBook = session.query(Book).filter_by(id=book_id).one()
    if editedAuthor.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit books by this author. Please create your own author in order to edit books.');history.back();}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if request.form['picture']:
            editedBook.picture = request.form['picture']
        if request.form['description']:
            editedBook.description = request.form['description']
        if request.form['price']:
            editedBook.price = request.form['price']
        session.add(editedBook)
        session.commit()
        flash('Book Successfully Edited: %s' % editedBook.name, "alert-success")
        return redirect(url_for('showBooks', author_id=author_id))
    else:
        return render_template('editBook.html', author=editedAuthor,
                               book=editedBook)

# Main function and flask app set up
if __name__ == '__main__':
    app.secret_key = 'super_secret_key' # Not recomended for producation use
    app.debug = True # Not recomended for producation use
    app.run(host='0.0.0.0', port=8000) # Port and host infromation

