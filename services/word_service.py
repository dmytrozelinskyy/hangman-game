from sqlalchemy.orm import Session
from models.word import Category, Word
from database import SessionLocal
import random


# -- Add New Category -- #
def add_category(category_name: str) -> bool:
    with SessionLocal() as session:
        # -- Check if category already exists -- #
        if session.query(Category).filter_by(name=category_name).first():
            return False
        session.add(Category(name=category_name))
        session.commit()
        return True


# -- Add New Word -- #
def add_word(word: str, category_name: str) -> bool:
    with SessionLocal() as session:
        # -- Check if word already exists -- #
        if session.query(Word).filter_by(word=word).first():
            return False

        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            return False

        session.add(Word(word=word, category_id=category.id))
        session.commit()
        return True


# -- Get Random Word -- #
def get_random_word(category_name: str = None) -> str | None:
    with SessionLocal() as session:
        if category_name and category_name.lower() != "random":
            category = session.query(Category).filter_by(name=category_name).first()
            if not category:
                return None
            words = session.query(Word).filter_by(category_id=category.id).all()
        else:
            words = session.query(Word).all()

        if not words:
            return None

        return random.choice(words).word


# -- Get All Categories -- #
def get_categories():
    with SessionLocal() as session:
        return [cat.name for cat in session.query(Category).all()]


# -- Get Words by Category -- #
def get_words_by_category(category_name: str):
    with SessionLocal() as session:
        category = session.query(Category).filter_by(name=category_name).first()
        if not category:
            return []
        words = session.query(Word).filter_by(category_id=category.id).all()
        return [word.word for word in words]
