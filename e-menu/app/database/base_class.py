from sqlalchemy import Column, DateTime, Integer
from datetime import datetime

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime(timezone=True), default=datetime.now)
    date_updated = Column(DateTime(timezone=True), onupdate=datetime.now)
