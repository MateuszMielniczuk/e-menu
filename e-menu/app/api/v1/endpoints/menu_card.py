from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status, Path
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


def validate_order_parameters(parameters: list):
    options = ["name", "nr_of_dishes"]
    operators = ["asc", "desc", ""]
    order_dict = dict()
    for param in parameters:
        k, *v = param.split("[")
        if k not in options or k in order_dict.keys():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bad option name for order_by or two same operators specified. Valid are: name, nr_of_dishes.",
            )
        if not v:
            order_dict[k] = ""
        else:
            if v[0][:-1] not in operators:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Bad operator name for order_by. Valid are: [asc], [desc] or None",
                )
            order_dict[k] = v[0][:-1]
    return order_dict


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
    menu_cards = get_menu_cards(
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
    menu = get_menu_by_id(db=db, id=id).first()
    if not menu:
        raise not_found_menu_exception(id)
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
    name_exists = check_unique_name(db=db, name=request.name)
    if name_exists:
        raise unique_name_exception(request.name)
    menu = create_menu(db=db, request=request)
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
    db_menu = get_menu_by_id(db=db, id=id)
    if not db_menu.first():
        raise not_found_menu_exception(id)
    name_exists = check_unique_name(db=db, name=request.name)
    if name_exists:
        raise unique_name_exception(request.name)
    update_menu(db=db, db_menu=db_menu, request=request)
    return db_menu.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete existing menu card")
def delete_menu_card(
    id: int = Path(description="The ID of the menu item to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete existing menu card"""
    db_menu = get_menu_by_id(db=db, id=id).first()
    if not db_menu:
        raise not_found_menu_exception(id)
    delete_menu(db=db, db_menu=db_menu)


@router.post("/{id_menu}/dish={id_dish}", status_code=status.HTTP_201_CREATED, summary="Add dish to menu card")
def add_dish_to_menu(
    id_menu: int = Path(description="The ID of the menu item"),
    id_dish: int = Path(description="The ID of the dish item to add"),
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
