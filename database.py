from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# -- Create Database Engine -- #
engine = create_engine('sqlite:///hangman.db', echo=False)

# -- Create Base class for Models -- #
Base = declarative_base()

# -- Session Factory -- #
SessionLocal = sessionmaker(bind=engine)
