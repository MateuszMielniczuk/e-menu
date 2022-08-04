from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.api.v1.endpoints.dish import not_found_exception as not_found_dish_exception
from app.crud.dish import get_dish_by_id
from app.crud.menu_card import (
    append_dish,
    check_unique_name,
    create_menu,
    delete_menu,
    get_menu_by_id,
    get_menu_cards,
    remove_dish,
    update_menu,
)
from app.models.user import User as UserModel
from app.schemas.menu_card import MenuCard, MenuCreate, MenuUpdate

router = APIRouter()


def not_found_menu_exception(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu with ID: '{id}' not found in database",
    )


def unique_name_exception(name: str):
    return HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"Menu card name: '{name}' exists. Name must be unique!",
    )


@router.get("", response_model=list[MenuCard], summary="Show by default non empty menu cards")
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
    menu = get_menu_by_id(db=db, id=id).first()
    if not menu:
        raise not_found_menu_exception(id)
    return menu


@router.post("", response_model=MenuCard, status_code=status.HTTP_201_CREATED)
def create_menu_card(
    request: MenuCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create new menu card
    - **name**: each item must have unique name
    """
    name_exists = check_unique_name(db=db, name=request.name)
    if name_exists:
        raise unique_name_exception(request.name)
    menu = create_menu(db=db, request=request)
    return menu


@router.put("/{id}", response_model=MenuCard)
def update_menu_card(
    id: int,
    request: MenuUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update existing menu card"""
    db_menu = get_menu_by_id(db=db, id=id)
    if not db_menu.first():
        raise not_found_menu_exception(id)
    name_exists = check_unique_name(db=db, name=request.name)
    if name_exists:
        raise unique_name_exception(request.name)
    update_menu(db=db, db_menu=db_menu, request=request)
    return db_menu.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_card(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete existing menu card"""
    db_menu = get_menu_by_id(db=db, id=id).first()
    if not db_menu:
        raise not_found_menu_exception(id)
    delete_menu(db=db, db_menu=db_menu)


@router.post("/{id_menu}/dish={id_dish}", status_code=status.HTTP_201_CREATED)
def add_dish_to_menu(
    id_menu: int,
    id_dish: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Add dish to menu card"""
    db_menu = get_menu_by_id(db, id_menu).first()
    if not db_menu:
        raise not_found_menu_exception(id_menu)
    db_dish = get_dish_by_id(db, id_dish).first()
    if not db_dish:
        raise not_found_dish_exception(id_dish)
    if db_dish in db_menu.dishes:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Dish already in menu!",
        )
    append_dish(db=db, db_dish=db_dish, db_menu=db_menu)
    return "Dish successfully added to menu"


@router.delete("/{id_menu}/dish={id_dish}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dish_from_menu(
    id_menu: int,
    id_dish: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete dish from menu card"""
    db_menu = get_menu_by_id(db, id_menu).first()
    if not db_menu:
        raise not_found_menu_exception(id_menu)
    db_dish = get_dish_by_id(db, id_dish).first()
    if not db_dish:
        raise not_found_dish_exception(id_dish)
    if db_dish not in db_menu.dishes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish not found in selected menu!",
        )
    remove_dish(db=db, db_dish=db_dish, db_menu=db_menu)
    return "Dish successfully removed from menu"
