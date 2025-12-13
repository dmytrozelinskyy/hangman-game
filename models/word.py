from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Word(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
