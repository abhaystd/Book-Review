from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookCreate(BaseModel):
    title: str
    author: str
    published_date: date
    isbn: str
    genre: Optional[str] = None
    price: Optional[float] = None

    model_config = {"from_attributes": True}

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    average_rating: float

    model_config = {"from_attributes": True}

class ReviewCreate(BaseModel):
    content: str
    rating: float = Field(..., ge=0.0, le=5.0)

    model_config = {"from_attributes": True}

class ReviewResponse(ReviewCreate):
    id: int
    book_id: int

    model_config = {"from_attributes": True}
