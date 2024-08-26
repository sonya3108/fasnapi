from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field


class NewProduct(BaseModel):
    title: str
    price: float = Field(gt=0, le=10_000, examples=[125.15])
    description: str
    cover: HttpUrl


class SavedProduct(NewProduct):
    id: int
    created_at: datetime