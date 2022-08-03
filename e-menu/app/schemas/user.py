from typing import Optional, Union

from pydantic import BaseModel  # , EmailStr


class UserBase(BaseModel):
    email: Optional[str]


class UserCreate(UserBase):
    email: str
    not_hashed_password: str


class UserInDBBase(UserBase):
    id: Optional[str] = None

    class Config:
        orm_mode = True


class User(UserInDBBase):
    ...


class UserInDB(UserInDBBase):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
