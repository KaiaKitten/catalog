from sqlalchemy import Column, ForeignKey, Integer, String, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Table to hold all users
class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))
    
# Table to hold all authors, used to categorize books
class Author(Base):
    __tablename__ = 'author'
        
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }
    
# Table to hold books categorize by author
class Book(Base):
    __tablename__ = 'book'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(REAL)
    picture = Column(String(250))
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship(Author)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'price': self.price,
            'picture': self.picture,
        }
    
engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
