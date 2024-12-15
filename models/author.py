from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import session
from database.connection import Base


class Author(Base):
    __tablename__="authors"

    id = Column(Integer, primary_key=True)
    name=Column(String, nullable=False)

    article =relationship('Article', backref="author")

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f'<Author {self.name}>'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        if hasattr(self,"name"):
            raise ValueError("name cannot be re-assgned")
        if not isinstance(name,str) and not len(name)> 0:
            raise ValueError("name must be a string")
        self._name =name

    def articles(self,session):
        return session.query(Article).join(Author).filter(Article.author_id ==self.id).all()

    def magazines(self,session):
        return session.query(Magazine).join(Author).filter(Article.author_id == self.id).all()