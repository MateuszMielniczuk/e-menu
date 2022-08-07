from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core import exceptions
from app.core.utils import validate_order_parameters
from app.crud import menu_card as crud_menu
from app.crud.dish import get_dish_by_id
from app.models.user import User as UserModel
from app.schemas.menu_card import MenuCard, MenuCreate, MenuUpdate

router = APIRouter()


@router.get("", response_model=list[MenuCard], summary="Show by default non empty menu cards")
def show_menu_cards(
    db: Session = Depends(get_db),
    is_empty: bool = Query(
        default=True,
        description="If value is True not showing empty menu cards",
    ),
    order_by: list[str] = Query(
        default=None,
        description="Order items. Available options are: name, nr_of_dishes. Operators: [asc], [desc].",
    ),
    name: Optional[str] = Query(
        default=None,
        description="Filter menu items by name.",
    ),
    date_created_gte: Optional[date] = Query(
        default=None,
        alias="date_created[gte]",
        description="Filter menu by date greater than or equal input value. Valid type is YYYY-MM-DD",
    ),
    date_created_lte: Optional[date] = Query(
        default=None,
        alias="date_created[lte]",
        description="Filter menu by date less than or equal input value. Valid type is YYYY-MM-DD",
    ),
    date_updated_gte: Optional[date] = Query(
        default=None,
        alias="date_updated[gte]",
        description="Filter menu by date greater than or equal input value. Valid type is YYYY-MM-DD",
    ),
    date_updated_lte: Optional[date] = Query(
        default=None,
        alias="date_updated[lte]",
        description="Filter menu by date less than or equal input value. Valid type is YYYY-MM-DD",
    ),
):
    """Show non empty menu cards"""
    if order_by:
        order_by = validate_order_parameters(order_by)
    menu_cards = crud_menu.get_menu_cards(
        db=db,
        is_empty=is_empty,
        name=name,
        date_created_gte=date_created_gte,
        date_created_lte=date_created_lte,
        date_updated_gte=date_updated_gte,
        date_updated_lte=date_updated_lte,
        order_by=order_by,
    )
    return menu_cards


@router.get("/{id}", response_model=MenuCard, summary="Show menu card detail by")
def get_menu_detail(
    id: int = Path(title="The ID of the menu item to get"),
    db: Session = Depends(get_db),
):
    menu = crud_menu.get_menu_by_id(db=db, id=id).first()
    if not menu:
        raise exceptions.menu_not_found_exception(id)
    return menu


@router.post("", response_model=MenuCard, status_code=status.HTTP_201_CREATED, summary="Create new menu card")
def create_menu_card(
    request: MenuCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """
    Create new menu card
    - **name**: each item must have unique name
    """
    name_exists = crud_menu.check_unique_name(db=db, name=request.name)
    if name_exists:
        raise exceptions.menu_unique_name_exception(request.name)
    menu = crud_menu.create_menu(db=db, request=request)
    return menu


@router.put("/{id}", response_model=MenuCard, summary="Update existing menu card")
def update_menu_card(
    *,
    id: int = Path(title="The ID of the menu item to update"),
    request: MenuUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update existing menu card"""
    db_menu = crud_menu.get_menu_by_id(db=db, id=id)
    if not db_menu.first():
        raise exceptions.menu_not_found_exception(id)
    name_exists = crud_menu.check_unique_name(db=db, name=request.name)
    if name_exists:
        raise exceptions.menu_unique_name_exception(request.name)
    crud_menu.update_menu(db=db, db_menu=db_menu, request=request)
    return db_menu.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete existing menu card")
def delete_menu_card(
    id: int = Path(description="The ID of the menu item to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete existing menu card"""
    db_menu = crud_menu.get_menu_by_id(db=db, id=id).first()
    if not db_menu:
        raise exceptions.menu_not_found_exception(id)
    crud_menu.delete_menu(db=db, db_menu=db_menu)


@router.post("/{id_menu}/dish={id_dish}", status_code=status.HTTP_201_CREATED, summary="Add dish to menu card")
def add_dish_to_menu(
    id_menu: int = Path(description="The ID of the menu item"),
    id_dish: int = Path(description="The ID of the dish item to add"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Add dish to menu card"""
    db_menu = crud_menu.get_menu_by_id(db, id_menu).first()
    if not db_menu:
        raise exceptions.menu_not_found_exception(id_menu)
    db_dish = get_dish_by_id(db, id_dish).first()
    if not db_dish:
        raise exceptions.dish_not_found_exception(id_dish)
    if db_dish in db_menu.dishes:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Dish already in menu!",
        )
    crud_menu.append_dish(db=db, db_dish=db_dish, db_menu=db_menu)
    return "Dish successfully added to menu"


@router.delete(
    "/{id_menu}/dish={id_dish}", status_code=status.HTTP_204_NO_CONTENT, summary="Remove dish from menu card"
)
def delete_dish_from_menu(
    id_menu: int = Path(description="The ID of the menu item"),
    id_dish: int = Path(description="The ID of the dish item to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete dish from menu card"""
    db_menu = crud_menu.get_menu_by_id(db, id_menu).first()
    if not db_menu:
        raise exceptions.menu_not_found_exception(id_menu)
    db_dish = get_dish_by_id(db, id_dish).first()
    if not db_dish:
        raise exceptions.dish_not_found_exception(id_dish)
    if db_dish not in db_menu.dishes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dish not found in selected menu!",
        )
    crud_menu.remove_dish(db=db, db_dish=db_dish, db_menu=db_menu)
    return "Dish successfully removed from menu"
