from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.crud.dish import get_dish_by_id
from app.models.menu_card import MenuCard as MenuCardModel
from app.schemas.menu_card import MenuCreate, MenuUpdate


def check_unique_name(db: Session, name: str):
    if db.query(MenuCardModel).filter(MenuCardModel.name == name).first():
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Menu card name: {name} exists. Name must be unique!",
        )


def get_menu_by_id(db: Session, id: int):
    menu = db.query(MenuCardModel).filter(MenuCardModel.id == id)
    if not menu.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu object with ID: {id} not found in database",
        )
    return menu


def get_menu(db: Session):
    return db.query(MenuCardModel).all()


def create_menu(request: MenuCreate, db: Session):
    check_unique_name(db=db, name=request.name)
    new_menu = MenuCardModel(
        name=request.name,
        description=request.description,
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def update_menu(db: Session, id: int, request: MenuUpdate):
    db_object = get_menu_by_id(db=db, id=id)
    request = dict(request)
    db_object.update(request)
    db.commit()
    return "Resource successfully updated"


def delete_menu(db: Session, id: int):
    db_object = get_menu_by_id(db=db, id=id)
    db_object.delete(synchronize_session=False)
    db.commit()
    return "Resource successfully deleted"


def append_dish(db: Session, id_menu: int, id_dish: int):
    menu = get_menu_by_id(db, id_menu).first()
    dish = get_dish_by_id(db, id_dish).first()
    if dish in menu.dishes:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Dish already in menu!",
        )
    menu.dishes.append(dish)
    db.commit()


def remove_dish(db: Session, id_menu: int, id_dish: int):
    menu = get_menu_by_id(db, id_menu).first()
    dish = get_dish_by_id(db, id_dish).first()
    if dish not in menu.dishes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish not found in selected menu!",
        )
    menu.dishes.remove(dish)
    db.commit()
