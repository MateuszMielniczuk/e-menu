from datetime import date

from sqlalchemy import Date, cast, desc, select
from sqlalchemy.orm import Session

from app.models.dish import Dish as DishModel
from app.models.menu_card import MenuCard as MenuCardModel
from app.schemas.menu_card import MenuCreate, MenuUpdate


def check_unique_name(db: Session, name: str):
    return db.query(MenuCardModel).filter(MenuCardModel.name == name).first()


def get_menu_by_id(db: Session, id: int):
    return db.query(MenuCardModel).filter(MenuCardModel.id == id)


def get_menu_cards(
    db: Session,
    is_empty: bool,
    name: str,
    date_created_gte: date,
    date_created_lte: date,
    date_updated_gte: date,
    date_updated_lte: date,
    order_by: dict,
):
    menu = select(MenuCardModel)
    if is_empty:
        menu = menu.filter(MenuCardModel.dishes != None)  # noqa E711
    if name:
        menu = menu.filter(MenuCardModel.name.ilike(f"%{name}%"))
    if date_created_gte:
        menu = menu.filter(cast(MenuCardModel.date_created, Date) >= date.strftime(date_created_gte, "%Y-%m-%d"))
    if date_created_lte:
        menu = menu.filter(cast(MenuCardModel.date_created, Date) <= date.strftime(date_created_lte, "%Y-%m-%d"))
    if date_updated_gte:
        menu = menu.filter(cast(MenuCardModel.date_updated, Date) >= date.strftime(date_updated_gte, "%Y-%m-%d"))
    if date_updated_lte:
        menu = menu.filter(cast(MenuCardModel.date_updated, Date) <= date.strftime(date_updated_lte, "%Y-%m-%d"))
    if order_by:
        if "name" in order_by.keys():
            if order_by["name"] == "desc":
                menu = menu.order_by(MenuCardModel.name.desc())
            else:
                menu = menu.order_by(MenuCardModel.name)
        if "nr_of_dishes" in order_by.keys():
            if order_by["nr_of_dishes"] == "desc":
                menu = menu.order_by(desc(MenuCardModel.dish_count))
            else:
                menu = menu.order_by(MenuCardModel.dish_count)
    return db.execute(menu).scalars().all()


def create_menu(request: MenuCreate, db: Session):
    new_menu = MenuCardModel(
        name=request.name,
        description=request.description,
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu


def update_menu(db: Session, db_menu: MenuCardModel, request: MenuUpdate):
    request = dict(request)
    db_menu.update(request)
    db.commit()
    return "Resource successfully updated"


def delete_menu(db: Session, db_menu: MenuCardModel):
    db.delete(db_menu)
    db.commit()
    return "Resource successfully deleted"


def append_dish(db: Session, db_menu: MenuCardModel, db_dish: DishModel):
    db_menu.dishes.append(db_dish)
    db.commit()
    return "Dish successfully added to menu"


def remove_dish(db: Session, db_menu: MenuCardModel, db_dish: DishModel):
    db_menu.dishes.remove(db_dish)
    db.commit()
    return "Dish successfully removed from menu"
