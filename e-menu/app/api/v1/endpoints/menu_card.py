from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.crud.menu_card import (
    append_dish,
    create_menu,
    delete_menu,
    get_menu_by_id,
    get_menu_cards,
    remove_dish,
    update_menu,
)
from app.database.session import get_db
from app.schemas.menu_card import MenuCard, MenuCreate, MenuUpdate

router = APIRouter()


@router.get("/", response_model=list[MenuCard], summary="Show by default non empty menu cards")
def show_menu_cards(
    db: Session = Depends(get_db),
    not_empty: bool = Query(description="If value is True not showing empty menu cards", default=True),
    name: Optional[str] = None,
    date_created: Optional[date] = None,
    date_updated: Optional[date] = None,
):
    """Show non empty menu cards"""
    menu_cards = get_menu_cards(
        db=db, not_empty=not_empty, name=name, date_created=date_created, date_updated=date_updated
    )
    return menu_cards


@router.get("/{id}", response_model=MenuCard)
def get_menu_detail(id: int, db: Session = Depends(get_db)):
    menu = get_menu_by_id(db=db, id=id)
    return menu.first()


@router.post("/", response_model=MenuCard, status_code=status.HTTP_201_CREATED)
def create_menu_card(request: MenuCreate, db: Session = Depends(get_db)):
    """
    Create new menu card
    - **name**: each item must have unique name
    """
    menu = create_menu(db=db, request=request)
    return menu


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_menu_card(*, db: Session = Depends(get_db), id: int, request: MenuUpdate):
    """Update existing menu card"""
    update_menu(db=db, id=id, request=request)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_card(id: int, db: Session = Depends(get_db)):
    """Delete existing menu card"""
    delete_menu(db=db, id=id)


@router.post("/{id_menu}/dish={id_dish}", status_code=status.HTTP_201_CREATED)
def add_dish_to_menu(id_menu: int, id_dish: int, db: Session = Depends(get_db)):
    """Add dish to menu card"""
    append_dish(db=db, id_menu=id_menu, id_dish=id_dish)
    return "Dish successfully added to menu"


@router.delete("/{id_menu}/dish={id_dish}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish_from_menu(id_menu: int, id_dish: int, db: Session = Depends(get_db)):
    """Delete dish from menu card"""
    remove_dish(db=db, id_menu=id_menu, id_dish=id_dish)
    return "Dish successfully removed from menu"
