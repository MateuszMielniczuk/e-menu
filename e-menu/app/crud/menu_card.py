# from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.menu_card import MenuCard as MenuCardModel
from app.schemas.menu_card import MenuCreate


def get_menu(db: Session):
    return db.query(MenuCardModel).all()


def create_menu(request: MenuCreate, db: Session):
    menu_card = db.query(MenuCardModel).filter(MenuCardModel.name == request.name).first()
    if menu_card:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Menu card name exists. Name must be unique!"
        )
    new_menu = MenuCardModel(
        name=request.name,
        description=request.description,
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu
