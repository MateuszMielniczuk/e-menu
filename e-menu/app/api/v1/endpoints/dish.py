from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.crud.dish import (
    create_dish,
    delete_dish,
    get_dish,
    get_dish_by_id,
    update_dish,
)
from app.models.user import User as UserModel
from app.schemas.dish import Dish, DishCreate, DishUpdate

router = APIRouter()


def not_found_exception(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish with ID: {id} not found in database",
    )


@router.get("", response_model=list[Dish], summary="Show all dishes stored in database")
def show_all_dishes(db: Session = Depends(get_db)):
    dish = get_dish(db)
    return dish


@router.post("", response_model=Dish, status_code=status.HTTP_201_CREATED, summary="Create new dish")
def create_new_dish(
    request: DishCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Create new dish"""
    dish = create_dish(request, db)
    return dish


@router.put("/{id}", response_model=Dish, summary="Update existing dish")
def update_dish_item(
    *,
    id: int = Path(description="The ID of the dish item to update"),
    request: DishUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Update existing dish"""
    db_dish = get_dish_by_id(db=db, id=id)
    if not db_dish.first():
        raise not_found_exception(id)
    update_dish(db=db, db_dish=db_dish, request=request)
    return db_dish.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete existing dish object")
def delete_dish_item(
    *,
    id: int = Path(description="The ID of the dish item to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    """Delete existing dish database"""
    db_dish = get_dish_by_id(db=db, id=id).first()
    if not db_dish:
        raise not_found_exception(id)
    delete_dish(db=db, db_dish=db_dish)
