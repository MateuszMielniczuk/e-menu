from datetime import date

from sqlalchemy import Date, cast, select
from sqlalchemy.orm import Session

from app.models.dish import Dish as DishModel
from app.models.menu_card import MenuCard as MenuCardModel
from app.schemas.menu_card import MenuCreate, MenuUpdate


def check_unique_name(db: Session, name: str):
    return db.query(MenuCardModel).filter(MenuCardModel.name == name).first()


def get_menu_by_id(db: Session, id: int):
    return db.query(MenuCardModel).filter(MenuCardModel.id == id)


def get_menu_cards(db: Session, not_empty: bool, name: str, date_created: date, date_updated: date):
    menu = select(MenuCardModel)
    if not_empty:
        menu = menu.filter(MenuCardModel.dishes != None)  # noqa E711
    if name:
        menu = menu.filter(MenuCardModel.name.ilike(f"%{name}%"))
    if date_created:
        menu = menu.filter(cast(MenuCardModel.date_created, Date) == date.strftime(date_created, "%Y-%m-%d"))
    if date_updated:
        menu = menu.filter(cast(MenuCardModel.date_updated, Date) == date.strftime(date_updated, "%Y-%m-%d"))
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
