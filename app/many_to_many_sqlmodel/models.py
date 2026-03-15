from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class AuthorBookLink(SQLModel, table=True):
    author_id: Optional[int] = Field(
        default=None, foreign_key="author.id", primary_key=True)
    book_id: Optional[int] = Field(
        default=None, foreign_key="book.id", primary_key=True)


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship to link Author with multiple books through a junction table
    books: List["Book"] = Relationship(
        back_populates="authors", link_model=AuthorBookLink)


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int

    authors: List["Author"] = Relationship(
        back_populates="books", link_model=AuthorBookLink)
