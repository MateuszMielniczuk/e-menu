from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User as UserModel


class User(BaseModel):
    id: int
    email: EmailStr
    password: str


class UserShow(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserInDB(UserShow):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, email: str):
    user = db.query(UserModel).filter(UserModel.email == email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email: {email} not found!",
        )
    return UserInDB(**user.first()._asdict())



def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
