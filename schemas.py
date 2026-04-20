from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    description: str


class ReviewCreate(BaseModel):
    book_id: int
    user_name: str
    rating: int
    comment: str
