from sqlalchemy.orm import Session

from app.models.dish import Dish as DishModel
from app.schemas.dish import DishCreate, DishUpdate


def get_dish(db: Session):
    return db.query(DishModel).all()


def get_dish_by_id(db: Session, id: int):
    return db.query(DishModel).filter(DishModel.id == id)


def create_dish(request: DishCreate, db: Session):
    dish_item = DishModel(
        name=request.name,
        description=request.description,
        price=request.price,
        preparation_time=request.preparation_time,
        is_vegan=request.is_vegan,
    )
    db.add(dish_item)
    db.commit()
    db.refresh(dish_item)
    return dish_item


def update_dish(db: Session, db_dish: DishModel, request: DishUpdate):
    request = dict(request)
    db_dish.update(request)
    db.commit()
    return "Resource successfully updated"


def delete_dish(db: Session, db_dish: DishModel):
    db.delete(db_dish)
    db.commit()
    return "Resource successfully deleted"
