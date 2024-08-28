from datetime import datetime

from pydantic import BaseModel, HttpUrl, Field


class ProductPrice(BaseModel):
    price: float = Field(gt=0, le=10_000, examples=[125.15])


class NewProduct(ProductPrice):
    title: str
    description: str
    cover: HttpUrl


class SavedProduct(NewProduct):
    id: int
    created_at: datetime


class DeletedProduct(BaseModel):
    id: int
    deleted: bool = True