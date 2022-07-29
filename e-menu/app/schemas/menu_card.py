from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class MenuCard(BaseModel):
    id: int = Field(description="Menu card database ID")
    name: str = Field(description="Menu card name")
    description: Optional[str] = Field(description="Menu card description")
    date_created: datetime = Field(description="Menu card creation date")
    date_updated: Optional[datetime] = Field(description="Menu card last update date")

    class Config:
        orm_mode = True
        title = "Menu card"
        schema_extra = {"example": {"id": 1, "name": "Lunch menu", "description": "-"}}


class MenuCreate(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class MenuUpdate(BaseModel):
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
