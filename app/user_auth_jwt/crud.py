from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate
from .database import SessionLocal


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, email=user.email,
                   hashed_password=user.password)
    db.add(db_user)
    db.commit()
