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


@app.post("/authors/")
def create_author(author: Author, session: Session = Depends(get_session)):
    author = Author(name="J.K. Rowling", book=[Book(title="Harry Potter and the Sorcerer's Stonr", year=1997), Book(
        title="Happy Potter and the Chamber of Secrets", year=1998)])
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@app.get("/authors/", response_model=List[AuthorRead])
def read_authors(session: Session = Depends(get_session)):
    authors = session.exec(
        select(Author).options(selectinload(Author.books))
    ).all()
    return authors


def insert_data():
    with Session(engine) as session:
        author = Author(name="J.K. Rowling", books=[
            Book(title="Happy Potter and the Sorcerer's Stone", year=1997),
            Book(title="Happy Potter and the Chamber of Secrets", year=1998)
        ])
        session.add(author)
        session.commit()


insert_data()
