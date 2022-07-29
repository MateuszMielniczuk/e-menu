from sqlalchemy.orm import Session

from app.models.dish import Dish as DishModel


def get_dish(db: Session):
    return db.query(DishModel).all()
