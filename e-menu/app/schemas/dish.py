from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DishBase(BaseModel):
    name: str = Field(description="Dish name")
    description: Optional[str] = Field(description="Dish description")
    price: Optional[float] = Field(description="Dish price")
    preparation_time: Optional[int] = Field(description="Time to prepare the dish in minutes")
    is_vegan: Optional[bool] = Field(description="Dish is vegan if value is True")


class Dish(DishBase):
    id: int = Field(description="Dish database ID")
    date_created: datetime = Field(description="Menu card creation date")
    date_updated: datetime = Field(description="Menu card last update date")

    class Config:
        orm_mode = True
        title = "Dish"
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Tomato soup",
                "description": "From fresh tomatoes and with noodles",
                "price": 12.50,
                "preparation_time": 10,
                "is_vegan": True,
            }
        }


class DishCreate(DishBase):
    ...


class DishUpdate(DishBase):
    ...
