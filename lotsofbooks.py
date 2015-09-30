from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Author, Book

engine = create_engine('sqlite:///restaurantmenuwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

author1 = Author(name = "Jules Verne")

session.add(author1)
session.commit()

book1 = Book(name = "Around the World in 80 days", description = "they like go around the world in 80 days and stuff", price = "$5.99", author = author1)

session.add(book1)
session.commit()

author2 = Author(name = "Mark Twain")

session.add(author2)
session.commit()

author3 = Author(name = "William Shakespeare")

session.add(author3)
session.commit()
