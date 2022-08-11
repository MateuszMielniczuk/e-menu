import secrets

from fastapi import APIRouter, Depends, File, HTTPException, Path, UploadFile, status
from PIL import Image
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.core.config import settings
from app.core.exceptions import dish_not_found_exception
from app.crud.dish import (
    create_dish,
    delete_dish,
    get_dish,
    get_dish_by_id,
    update_dish,
    update_dish_image,
)
from app.models.user import User as UserModel
from app.schemas.dish import Dish, DishCreate, DishUpdate

router = APIRouter()


@router.get("", response_model=list[Dish], summary="Show all dishes stored in database")
def show_all_dishes(db: Session = Depends(get_db)):
    dish = get_dish(db)
    return dish


@router.post("", response_model=Dish, status_code=status.HTTP_201_CREATED, summary="Create new dish")
def create_new_dish(
    *,
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
        raise dish_not_found_exception(id)
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
        raise dish_not_found_exception(id)
    delete_dish(db=db, db_dish=db_dish)


@router.post("/upload-image/{id}")
async def add_dish_image(
    id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_dish = get_dish_by_id(db=db, id=id)
    if not db_dish.first():
        raise dish_not_found_exception(id)
    image_name, extension = validate_image_filename(image.filename)

    IMAGE_PAHT = settings.STATIC_DIR + "/dish_images/"
    generated_img_name = image_name[:10] + secrets.token_hex(10) + "." + extension

    static_img_paht = IMAGE_PAHT + generated_img_name

    await save_image(path=static_img_paht, image=image)
    update_dish_image(db=db, db_dish=db_dish, path="/dish_images/" + generated_img_name)
    return {"filename": settings.BASE_URL + "/" + static_img_paht}


def validate_image_filename(filename):
    if "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Image file needs to have an extension",
        )
    image_name, *_, extension = filename.split(".")
    if extension not in ["jpg", "jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="Not allowed file extension. Pick: jped, jpg, png",
        )
    return image_name, extension


async def save_image(path: str, image: memoryview) -> None:
    file_content = await image.read()

    with open(path, "wb") as file:
        file.write(file_content)

    # Pillow
    img = Image.open(path)
    img = img.resize(size=(200, 200))
    img.save(path)

    image.close()
