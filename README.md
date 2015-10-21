Catalog
==============
Website/WebApp to display a list of categories each contanting a list of items (authors and books in example case).

Requirements
------------
* Python >= 2.7
* Flask >= 0.9 
* Flask-Login >= 0.1.3
* flask-seasurf >= 0.2.1
* dicttoxml >= 1.6.6
* httplib2 >= 0.9.1
* oauth2client >= 1.4.12
* requests >= 2.0.0
* SQLAlchemy >= 0.8.4
* werkzeug >= 0.8.3
* Linux assumed (or Vagrant), but should work on Mac and Windows.
* Vagrant(Optional)

Installation
------------
Clone repo:

	git clone https://github.com/kyahco/catalog.git catalog

#####Using Vagrant(Recommended)
Using Vagrant will asure there are no "It worked on my machine" problems.
Install vagrant [here](https://www.vagrantup.com/downloads.html)
    
Direct to the cloned repo, start up, and connect to Vagrant:
	
    cd catalog
    vagrant up
    vagrant ssh

Continue to Setup step

#####Without Vagrant

If you do not have python 2.7, install it [here](https://www.python.org/downloads/). See [here](http://flask.pocoo.org/docs/0.10/python3/) for information on python 3 support.

Direct to `catalog` folder.

Install requerments with pip:

	pip install -r requirements.txt
    
Continue to Setup step

Setup
-----
Set up database: 
	
    python database_setup.py
    
Fill database with example information (Optional):

	python lotsofbooks.py

Running
-----
Simply run `python project.py` and direct your browser to the domain assigned (defualt: localhost:8000)

Usage
-----
Click a category (author) to see the items (books) listed under it.

If logged in using your Google account (or create a new one) you can add/edit/delte categories as well as items in each category.

JSON and XML endpoints can be eached by appending /JSON or /XML to a URL for categories(authors), items(books) in a category, or each individual item(book).

![Screenshot of book items list in Jules Verne catagory](http://i.imgur.com/hZLeSPo.png)

Credits
-------

* Udacity for everything


