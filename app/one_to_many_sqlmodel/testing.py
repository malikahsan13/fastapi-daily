from fastapi import FastAPI, Depends
from sqlmodel import Session, select, SQLModel
from database import create_db_and_tables, engine
from models import Author, Book
from typing import Optional, List
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager


class BookRead(SQLModel):
    id: int
    title: str
    year: int


class AuthorRead(SQLModel):
    id: int
    name: str
    books: List[BookRead] = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session
