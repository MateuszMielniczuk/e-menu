from sqlalchemy import Column, ForeignKey, String, Table, Text, func, select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref, relationship

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

    dishes = relationship("Dish", secondary=menu_dish_junction, backref=backref("menus", lazy="joined"))

    def __repr__(self) -> str:
        return f"MenuCard: {self.name}"

    @hybrid_property
    def dish_count(self):
        if self.dishes:
            return len(self.dishes)
        return 0

    @dish_count.expression
    def dish_count(cls):
        return select([func.count(menu_dish_junction.c.dish_id)]).where(menu_dish_junction.c.menu_card_id == cls.id)
