from fastapi import HTTPException, status


def dish_not_found_exception(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish with ID: {id} not found in database",
    )


def menu_not_found_exception(id: int):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu with ID: '{id}' not found in database",
    )


def menu_unique_name_exception(name: str):
    return HTTPException(
        status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
        detail=f"Menu card name: '{name}' exists. Name must be unique!",
    )
