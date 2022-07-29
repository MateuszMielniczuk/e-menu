from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Dish(BaseModel):
    id: int = Field(description="Dish database ID")
    name: str = Field(description="Dish name")
    description: Optional[str] = Field(description="Dish description")
    price: Optional[float] = Field(description="Dish price")
    preparation_time: Optional[int] = Field(description="Time to prepare the dish in minutes")
    is_vegan: Optional[bool] = Field(description="Dish is vegan if value is True")
    date_created: datetime = Field(description="Menu card creation date")
    date_updated: datetime = Field(description="Menu card last update date")

    class Config:
        orm_mode = True
        title = "Dish"
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Lunch menu",
                "description": "-",
                "price": 12.50,
                "preparation_time": 10,
                "is_vegan": True,
            }
        }


class DishUpdate(BaseModel):
    id: int


class DishCreate(BaseModel):
    id: int
