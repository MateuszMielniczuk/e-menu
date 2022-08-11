from sqlalchemy import Boolean, Column, Integer, Numeric, String, Text

from app.core.config import settings
from app.database.base_class import Base


class Dish(Base):
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    preparation_time = Column(Integer)
    is_vegan = Column(Boolean, nullable=False)
    image_path = Column(String(2048), default="/default_dish.jpg")

    def __repr__(self) -> str:
        vegan = "dish is vegan!" if self.is_vegan else "not vegan!"
        return f"Name: {self.name}, price: {self.price}, {vegan}"

    @property
    def image_url(self) -> str:
        if self.image_path:
            return settings.BASE_URL + "/" + settings.STATIC_DIR + self.image_path
        return None
