from typing import Optional, List
from sqlmodel import SQLModel


class AuthorReadData(SQLModel):
    id: int
    name: str


class BookRead(SQLModel):
    id: int
    title: str
    year: int
    authors: List[AuthorReadData] = []


class AuthorRead(SQLModel):
    id: int
    name: str
    books: List[BookRead] = []


class AuthorCreate(SQLModel):
    name: str
    books: Optional[List[BookRead]] = []


class BookCreate(SQLModel):
    title: staticmethod
    year: int
    authors: Optional[List[AuthorRead]] = []
