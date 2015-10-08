from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Base, Author, Book

engine = create_engine('sqlite:///catalog.db')
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

book1 = Book(name = "Around the World in 80 days", description = "Donec arcu tellus, laoreet ac ornare ut, pharetra quis orci. Donec id eros eget massa tincidunt volutpat. Sed eget sodales arcu. Proin a hendrerit dolor. Vivamus ac tempus dui. Maecenas rutrum ultricies lacus ac dapibus. Pellentesque id cursus metus.", price = "5.99", author = author1)

session.add(book1)
session.commit()

book2 = Book(name = "To the Moon and Back", description = "Integer elit diam, dictum vel augue non, feugiat finibus leo. Phasellus tincidunt dui in ligula vestibulum, eget accumsan nisi scelerisque. In eu sagittis velit, non ornare justo. Sed et massa at lacus laoreet cursus. Praesent sit amet ex massa nunc.", price = "4.99", author = author1)

session.add(book2)
session.commit()

book3 = Book(name ="Journy to the Center of the Earth", description = "Vivamus vulputate nisl nec diam placerat maximus vel vitae nulla. Duis rutrum orci finibus aliquam aliquet. Duis ac metus nisl. Mauris non luctus enim. In sit amet cursus dui. Etiam sagittis elit felis, non pellentesque enim rutrum vel. Praesent sed.", price = "6.50", author = author1)

session.add(book3)
session.commit()

book4 = Book(name = "Children of Caption Grant", description = "Curabitur faucibus, urna vel imperdiet aliquet, lacus justo ultrices dui, ut aliquet velit turpis nec velit. Nullam at nunc diam. Nullam nibh nulla, euismod sed nunc quis, tristique maximus mi. Nulla auctor ligula auctor ornare ullamcorper. Sed amet.", price = "7.25", author = author1)

session.add(book4)
session.commit()

book5 = Book(name = "20 Thousand Leagues Under the Sea", description = "Nunc quis gravida erat. Integer posuere ex non ex pellentesque, ac vestibulum magna tincidunt. Integer porttitor tellus quis mattis ultricies. Aenean tortor odio, ullamcorper eget consequat nec, consequat ac justo. In et imperdiet mi. Class volutpat.", price = "5.00", author = author1)

session.add(book5)
session.commit()

author2 = Author(name = "Mark Twain")

session.add(author2)
session.commit()

author3 = Author(name = "William Shakespeare")

session.add(author3)
session.commit()
