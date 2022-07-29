from sqlalchemy import Column, String

from app.database.base_class import Base


class User(Base):
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
