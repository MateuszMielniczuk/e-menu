from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative, declared_attr

# from sqlalchemy.orm import declarative_base

# Base = declarative_base()


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), default=datetime.utcnow)
    date_updated = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
