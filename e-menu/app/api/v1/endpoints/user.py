from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.dependencies import authenticate_user, get_current_user, get_db
from app.core.utils import create_access_token
from app.crud.user import create, get_user_by_email
from app.models.user import User as UserModel
from app.schemas.user import Token, User, UserCreate
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.post("/access-token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.email, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create-user", response_model=User)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """Create new user"""
    user = get_user_by_email(db=db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400,
            detail="The user with this email already exists in database.",
        )
    user = create(db=db, user_in=user_in)
    return user


@router.post("/login/test-token", response_model=User)
def test_token(current_user: UserModel = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
