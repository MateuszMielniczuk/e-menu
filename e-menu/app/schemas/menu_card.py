from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    name: str
    description: Optional[str]

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

    class Config:
        orm_mode = True
        title = "Menu card"
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Lunch menu",
                "description": "From 11 to 13",
            }
        }


class MenuCreate(MenuBase):
    ...


class MenuUpdate(MenuBase):
    ...
