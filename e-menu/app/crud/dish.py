from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.dish import Dish as DishModel
from app.schemas.dish import DishCreate, DishUpdate


def get_dish(db: Session):
    return db.query(DishModel).all()


def get_dish_by_id(db: Session, id: int):
    dish = db.query(DishModel).filter(DishModel.id == id)
    if not dish.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu object with ID: {id} not found in database",
        )
    return dish


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


def update_dish(db: Session, id: int, request: DishUpdate):
    db_object = get_dish_by_id(db=db, id=id)
    request = dict(request)
    db_object.update(request)
    db.commit()
    return "Resource successfully updated"


def delete_dish(db: Session, id: int):
    db_object = get_dish_by_id(db=db, id=id)
    db_object.delete(synchronize_session=False)
    db.commit()
    return "Resource successfully deleted"
