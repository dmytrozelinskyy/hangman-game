from sqlalchemy.orm import Session
from models.user import User
from database import SessionLocal
import bcrypt
import secrets
import string


# ------------------------------------------- #
# --- Password Encryption and Decryption ---  #
# ------------------------------------------- #

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def generate_random_password(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))


# -- Get Existing User -- #
def get_user_by_credentials(username: str, password: str) -> User | None:
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(password, user.password):
            return user
        return None


def get_user_by_username(username: str) -> User | None:
    with SessionLocal() as session:
        return session.query(User).filter_by(username=username).first()


# -- Create User -- #
def create_user(name: str, surname: str, age: int, email: str,
                username: str, password: str) -> bool:
    with SessionLocal() as session:
        # -- Check if username already exists -- #
        if session.query(User).filter_by(username=username).first():
            return False
        # -- Check if email already exists -- #
        if session.query(User).filter_by(email=email).first():
            return False

        hashed_password = hash_password(password)
        user = User(name=name,
                    surname=surname,
                    age=age,
                    email=email,
                    username=username,
                    password=hashed_password)
        session.add(user)
        session.commit()
        return True


# -- Update User Score -- #
def update_score(username: str, increment: int = 1):
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.score += increment
            session.commit()


# -- Reset Password -- #
def reset_password(username: str) -> str | None:
    with SessionLocal() as session:
        user = session.query(User).filter_by(username=username).first()
        if user:
            new_password = generate_random_password()
            user.password = hash_password(new_password)
            session.commit()
            return new_password
        return None
