from sqlalchemy import Boolean, Column, Integer, Numeric, String, Text

from app.database.base_class import Base


class Dish(Base):
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    preparation_time = Column(Integer)
    is_vegan: bool = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        vegan = ", VEGAN!" if self.is_vegan else "."
        return f"{self.name}: price: {self.price}{vegan}"
