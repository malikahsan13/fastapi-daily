from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int
    author_id: Optional[int] = Field(default=None, foreign_key=True)

    author: Optional["Author"] = Relationship(back_populates="books")


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    books: List[Book] = Relationship(back_populates="author")
