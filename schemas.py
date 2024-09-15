# schemas.py
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field


class TripPrice(BaseModel):
    price: float = Field(gt=0, le=10000, examples=[100.50])


class NewTrip(TripPrice):
    title: str
    destination: str
    description: str
    image: HttpUrl


class SavedTrip(NewTrip):
    id: int
    created_at: datetime

