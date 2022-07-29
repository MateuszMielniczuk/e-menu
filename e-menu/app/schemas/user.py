from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr
    password: str


class UserShow(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
