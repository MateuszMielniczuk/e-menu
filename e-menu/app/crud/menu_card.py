from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.menu_card import MenuCard as MenuCardModel
from app.schemas.menu_card import MenuCreate, MenuUpdate


def get_menu_by_id(db: Session, id: int):
    menu = db.query(MenuCardModel).filter(MenuCardModel.id == id)
    if not menu.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu object with ID: {id} not found in database"
        )
    return menu


def get_menu(db: Session):
    return db.query(MenuCardModel).all()


def create_menu(request: MenuCreate, db: Session):
    menu_card = db.query(MenuCardModel).filter(MenuCardModel.name == request.name).first()
    if menu_card:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail=f"Menu card name: {request.name} exists. Name must be unique!",
        )
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