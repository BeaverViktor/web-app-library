from myapp.database import Base

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, backref

books_authors = Table('books_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
    )

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    
    books = relationship('Book', secondary=books_authors, backref='authors',
                         cascade='delete')
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Author('%s', '%s')>" % (self.id, self.name)

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "<Book('%s', '%s')>" % (self.id, self.name)