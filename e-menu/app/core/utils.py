from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: Union[str, Any], expires_delta: Union[timedelta, None] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def validate_order_parameters(parameters: list):
    options = ["name", "nr_of_dishes"]
    operators = ["asc", "desc", ""]
    order_dict = dict()
    for param in parameters:
        k, *v = param.split("[")
        if k not in options or k in order_dict.keys():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad option name for order_by or two same operators specified. Valid are: name, nr_of_dishes.",
            )
        if not v:
            order_dict[k] = ""
        else:
            if v[0][:-1] not in operators:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bad operator name for order_by. Valid are: [asc], [desc] or None",
                )
            order_dict[k] = v[0][:-1]
    return order_dict
