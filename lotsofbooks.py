from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Author, Book, User

# Script to add faux authors and books to database for testing

engine = create_engine('postgresql://postgres:password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

user1 = User(name="John Doe", email="JohnDoe@email.com",
             picture='http://i.imgur.com/1062ZiN.png')

session.add(user1)
session.commit()

author1 = Author(user_id=1, name = "Jules Verne")

session.add(author1)
session.commit()

book1 = Book(user_id=1, name = "Around the World in 80 days", description = "Donec arcu tellus, laoreet ac ornare ut, pharetra quis orci. Donec id eros eget massa tincidunt volutpat. Sed eget sodales arcu. Proin a hendrerit dolor. Vivamus ac tempus dui. Maecenas rutrum ultricies lacus ac dapibus. Pellentesque id cursus metus.",picture="https://upload.wikimedia.org/wikipedia/commons/8/86/Verne_Tour_du_Monde.jpg", price = "5.99", author = author1)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name = "To the Moon and Back", description = "Integer elit diam, dictum vel augue non, feugiat finibus leo. Phasellus tincidunt dui in ligula vestibulum, eget accumsan nisi scelerisque. In eu sagittis velit, non ornare justo. Sed et massa at lacus laoreet cursus. Praesent sit amet ex massa nunc.", price = "4.99", author = author1)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name ="Journy to the Center of the Earth", description = "Vivamus vulputate nisl nec diam placerat maximus vel vitae nulla. Duis rutrum orci finibus aliquam aliquet. Duis ac metus nisl. Mauris non luctus enim. In sit amet cursus dui. Etiam sagittis elit felis, non pellentesque enim rutrum vel. Praesent sed.", price = "6.50", picture="https://upload.wikimedia.org/wikipedia/commons/6/67/A_Journey_to_the_Centre_of_the_Earth-1874.jpg", author = author1)

session.add(book3)
session.commit()

book4 = Book(user_id=1, name = "Children of Caption Grant", description = "Curabitur faucibus, urna vel imperdiet aliquet, lacus justo ultrices dui, ut aliquet velit turpis nec velit. Nullam at nunc diam. Nullam nibh nulla, euismod sed nunc quis, tristique maximus mi. Nulla auctor ligula auctor ornare ullamcorper. Sed amet.", price = "7.25", author = author1)

session.add(book4)
session.commit()

book5 = Book(user_id=1, name = "20 Thousand Leagues Under the Sea", description = "Nunc quis gravida erat. Integer posuere ex non ex pellentesque, ac vestibulum magna tincidunt. Integer porttitor tellus quis mattis ultricies. Aenean tortor odio, ullamcorper eget consequat nec, consequat ac justo. In et imperdiet mi. Class volutpat.", price = "5.00", author = author1)

session.add(book5)
session.commit()

author2 = Author(user_id=1, name = "Mark Twain")
session.add(author2)
session.commit()

book6 = Book(user_id=1, name = "The Adventures of Tom Sawyer", description = "Donec arcu tellus, laoreet ac ornare ut, pharetra quis orci. Donec id eros eget massa tincidunt volutpat. Sed eget sodales arcu. Proin a hendrerit dolor. Vivamus ac tempus dui. Maecenas rutrum ultricies lacus ac dapibus. Pellentesque id cursus metus.", price = "7.99", author = author2)

session.add(book6)
session.commit()

book7 = Book(user_id=1, name = "Adventures of Huckleberry Finn", description = "Integer elit diam, dictum vel augue non, feugiat finibus leo. Phasellus tincidunt dui in ligula vestibulum, eget accumsan nisi scelerisque. In eu sagittis velit, non ornare justo. Sed et massa at lacus laoreet cursus. Praesent sit amet ex massa nunc.", price = "6.99", author = author2)

session.add(book7)
session.commit()

book8 = Book(user_id=1, name ="The Prince and the Pauper", description = "Vivamus vulputate nisl nec diam placerat maximus vel vitae nulla. Duis rutrum orci finibus aliquam aliquet. Duis ac metus nisl. Mauris non luctus enim. In sit amet cursus dui. Etiam sagittis elit felis, non pellentesque enim rutrum vel. Praesent sed.", price = "3.40", author = author2)

session.add(book8)
session.commit()

book9 = Book(user_id=1, name = "Life on the Mississippi", description = "Curabitur faucibus, urna vel imperdiet aliquet, lacus justo ultrices dui, ut aliquet velit turpis nec velit. Nullam at nunc diam. Nullam nibh nulla, euismod sed nunc quis, tristique maximus mi. Nulla auctor ligula auctor ornare ullamcorper. Sed amet.", price = "8.25", author = author2)

session.add(book9)
session.commit()

author3 = Author(user_id=1, name = "William Shakespeare")

session.add(author3)
session.commit()

book10 = Book(user_id=1, name = "Hamlet", description = "Curabitur faucibus, urna vel imperdiet aliquet, lacus justo ultrices dui, ut aliquet velit turpis nec velit. Nullam at nunc diam. Nullam nibh nulla, euismod sed nunc quis, tristique maximus mi. Nulla auctor ligula auctor ornare ullamcorper. Sed amet.", price = "10.25", author = author3)

session.add(book10)
session.commit()

book11 = Book(user_id=1, name = "Romeo and Juliet", description = "Curabitur faucibus, urna vel imperdiet aliquet, lacus justo ultrices dui, ut aliquet velit turpis nec velit. Nullam at nunc diam. Nullam nibh nulla, euismod sed nunc quis, tristique maximus mi. Nulla auctor ligula auctor ornare ullamcorper. Sed amet.", price = "11.25", author = author3)

session.add(book11)
session.commit()

book12 = Book(user_id=1, name = "Macbeth", description = "Curabitur faucibus, urna vel imperdiet aliquet, lacus justo ultrices dui, ut aliquet velit turpis nec velit. Nullam at nunc diam. Nullam nibh nulla, euismod sed nunc quis, tristique maximus mi. Nulla auctor ligula auctor ornare ullamcorper. Sed amet.", price = "19.99", author = author3)

session.add(book12)
session.commit()
