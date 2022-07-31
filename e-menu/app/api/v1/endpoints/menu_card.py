from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.crud.menu_card import create_menu, delete_menu, get_menu, update_menu
from app.database.session import get_db
from app.schemas.menu_card import MenuCard, MenuCreate, MenuUpdate

router = APIRouter()


@router.get("/", response_model=list[MenuCard])
def show_menu_card(db: Session = Depends(get_db)):
    """Show non empty menu cards menu cards"""
    menu = get_menu(db)
    return menu


@router.post("/", response_model=MenuCard, status_code=status.HTTP_201_CREATED)
def create_menu_card(request: MenuCreate, db: Session = Depends(get_db)):
    """Create new menu card"""
    menu = create_menu(request, db)
    return menu


@router.put("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def update_menu_card(*, db: Session = Depends(get_db), id: int, request: MenuUpdate):
    """Update existing menu card"""
    update_menu(db=db, id=id, request=request)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_card(*, db: Session = Depends(get_db), id: int):
    """Delete existing menu card"""
    delete_menu(db=db, id=id)
