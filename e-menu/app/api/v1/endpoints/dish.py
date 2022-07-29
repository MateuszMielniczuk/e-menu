from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.dish import get_dish
from app.database.session import get_db
from app.schemas.dish import Dish, DishCreate, DishUpdate

router = APIRouter()


@router.get("/", response_model=list[Dish])
def show_dish(db: Session = Depends(get_db)):
    dish = get_dish(db)
    return dish


@router.post("/", response_model=Dish, status_code=status.HTTP_201_CREATED)
def create_new_dish(request: DishCreate, db: Session = Depends(get_db)):
    """Create new dish"""
    # dish = create_dish(request, db)
    # return dish
    ...


@router.put("/{id}", response_model=Dish)
def update_dish(*, db: Session = Depends(get_db), id: int, request: DishUpdate):
    """Update existing dish"""
    ...


@router.delete("/{id}", response_model=Dish)
def delete_dish(*, db: Session = Depends(get_db), id: int):
    """Delete existing dish from db"""
    ...
