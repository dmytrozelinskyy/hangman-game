from models.user import User
from database import SessionLocal


# -- Get All Scores -- #
def get_all_scores():
    with SessionLocal() as session:
        users = session.query(User).order_by(User.score.desc()).all()
        return [(user.username, user.score) for user in users]


# -- Get Top Scores -- #
def get_top_scores(limit: int = 10):
    with SessionLocal() as session:
        users = session.query(User).order_by(User.score.desc()).all()
        return [(user.username, user.score) for user in users]


# -- Get User Rank -- #
def get_user_rank(username: str) -> int:
    with SessionLocal() as session:
        users = session.query(User).order_by(User.score.desc()).all()
        for i, user in enumerate(users, 1):
            if user.username == username:
                return i
        return -1