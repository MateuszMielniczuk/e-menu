from sqlalchemy import Column, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base_class import Base


menu_dish_junction = Table(
    "menu_dish_junction",
    Base.metadata,
    Column("menu_card_id", ForeignKey("menu_card.id"), primary_key=True),
    Column("dish_id", ForeignKey("dish.id"), primary_key=True),
)


class MenuCard(Base):
    __tablename__ = "menu_card"

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)

    dishes = relationship("Dish", secondary=menu_dish_junction, backref="menus")

    def __repr__(self) -> str:
        return f"MenuCard: {self.name}"
