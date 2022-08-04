from sqlalchemy.orm import Session

from app.core.utils import get_password_hash
from app.models.user import User as UserModel
from app.schemas.user import UserCreate


def get_user(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def create(db: Session, user_in: UserCreate) -> UserModel:
    db_user = UserModel(
        email=user_in.email,
        password=get_password_hash(user_in.not_hashed_password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
