from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.connection import session
from sqlalchemy.sql import func
from database.connection import Base
class Magazine(Base):
    __tablename__ = "magazines"

    id =Column(Integer,primary_key=True)
    name=Column(String,nullable=False,unique=True)
    Category=Column(String, nullable=False)

    articles= relationship('Article', backref="magazine")
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def __repr__(self):
        return f'<Magazine {self.name}>'
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        if not isinstance(name,str) and not 2 <=(len(name))<= 16:
            raise ValueError("name must be a string and between 2 an16 character long")
        self._name =name
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self,category):
        if not isinstance(category,str) and not len(name)> 0:
            raise ValueError("name must be a string and not empty")
        self._category =category
    def articles(self,session):
        return session.query(Article).join(Magazine).filter(Article.magazine_id==self.id).all()

    def contributors(self,session):
        return session.query(Author).join(Article).filter(Article.magazine_id==self.id).all()


    def article_titles(self):
        titles = [article.title for article in self.articles]
        return titles if titles else None

    def contributing_authors(self, session):
        results = (
            session.query(Author)
            .join(Article)
            .filter(Article.magazine_id == self.id)
            .group_by(Author.id)
            .having(func.count(Article.id) > 2)
            .all()
        )
        return results if results else None
