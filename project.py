from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Author, Book, User

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/author/')
def showAuthors():
    authors = session.query(Author).order_by(asc(Author.name))
    return render_template('authors.html', authors = authors)

@app.route('/author/new/', methods=['GET', 'POST'])    
def newAuthor():
    if request.method == 'POST':
        newAuthor = Author(name=request.form['name'])
        session.add(newAuthor)
        flash('New Author %s Successfully Added' % newAuthor.name)
        session.commit()
        return redirect(url_for('showAuthors'))
    else:
        return render_template('newAuthor.html')
        
@app.route('/author/<int:author_id>/edit', methods=['GET', 'POST'])        
def editAuthor(author_id):
    editedAuthor = session.query(Author).filter_by(id=author_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedAuthor.name = request.form['name']
            flash('Author Successfully Edited: %s' % editedAuthor.name)
            return redirect(url_for('showAuthors'))
    else:
        return render_template('editAuthor.html', author=editedAuthor)
        
@app.route('/author/<int:author_id>/delete', methods=['GET', 'POST'])
def deleteAuthor(author_id):
    authorDelete = session.query(
        Author).filter_by(id=author_id).one()
    if request.method == 'POST':
        session.delete(authorDelete)
        flash('Author Successfully Removed: %s' % authorDelete.name)
        session.commit()
        return redirect(url_for('showAuthors', author_id=author_id))
    else:
        return render_template('deleteAuthor.html', author=authorDelete)

@app.route('/author/<int:author_id>/')
@app.route('/author/<int:author_id>/books/')        
def showBooks(author_id):
    author = session.query(Author).filter_by(id=author_id).one()
    books = session.query(Book).filter_by(author_id=author_id).all()
    return render_template('books.html', books=books, author=author)
       
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    
