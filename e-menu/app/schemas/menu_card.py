from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.dish import Dish


class MenuBase(BaseModel):
    name: str = Field(description="Menu card name")
    description: Optional[str] = Field(description="Menu card description")

    class Config:
        schema_extra = {
            "example": {
                "name": "Menu Card name",
                "description": "Menu card description ...",
            }
        }


class MenuCard(MenuBase):
    id: int = Field(description="Menu card database ID")
    date_created: datetime = Field(description="Menu card creation date")
    date_updated: Optional[datetime] = Field(description="Menu card last update date")
    dishes: Optional[list[Dish]] = Field(description="Dishes list", default_factory=list)

    class Config:
        orm_mode = True
        title = "Menu card"
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Lunch menu",
                "description": "From 11 to 13",
                "date_created": "2022-07-31 22:42:45.636 +0000",
                "date_updated": "2022-07-31 22:46:37.162 +0000",
            }
        }


class MenuCreate(MenuBase):
    ...


class MenuUpdate(MenuBase):
    ...
