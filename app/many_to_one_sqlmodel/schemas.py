from typing import List, Optional
from sqlmodel import SQLModel


class BookRead(SQLModel):
    id: int
    title: str
    year: int


class PublisherRead(SQLModel):
    id: int
    name: str
    books: List[BookRead] = []
