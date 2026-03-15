from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Publisher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    books: List['Book'] = Relationship(back_populates="publisher")


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int

    publisher_id: Optional[int] = Field(default=None, foreign_key="publisher")
