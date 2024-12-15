from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database.connection import session
from database.connection import Base


class Article(Base):
    __tablename__ ="articles"

    id =Column(Integer,primary_key=True)
    title=Column(String(50), nullable=False)
    content=Column(String)
    author_id=Column(String, ForeignKey("authors.id"), nullable=False)
    magazine_id=Column(String, ForeignKey("magazines.id"),nullable=False)

    author = relationship("Author", backref="articles")
    magazine = relationship("Magazine", backref="articles")


    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self,title):
        if hasattr(self,"title"):
            raise ValueError("title cannot be re-assgned")
        if not isinstance(title,str) and not 5 <=(len(title))<=50:
            raise ValueError("title must be a string and be between 5 and 50 characters long")
        self._title =title

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise ValueError("Content must be a string.")
        self._content = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, magazine_instance):
        if not isinstance(magazine_instance, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        self._magazine = magazine_instance

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author_instance):
        if not isinstance(author_instance, Author):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        self._author = author_instance
    def get_author(self, session):
        return session.query(Author).filter(Author.id == self.author_id).first()

    def get_magazine(self, session):
        return session.query(Magazine).filter(Magazine.id == self.magazine_id).first()

    


    
    
