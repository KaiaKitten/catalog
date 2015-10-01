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
    
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
    
