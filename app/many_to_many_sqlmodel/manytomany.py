from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from typing import List
from database import create_db_and_tables, engine
from models import Author, Book, AuthorBookLink
from schemas import AuthorRead, BookRead, AuthorCreate, BookCreate
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager

# app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    insert_dummy_data()
    yield

app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


def insert_dummy_data():
    with Session(engine) as session:
        if not session.exec(select(Author)).first()
        # Insert authors and books with relationships
        author1 = Author(name="J.K.Rowling")
        author2 = Author(name="George R.R. Martin")
        book1 = Book(title="Happy Potter and the Sorcerer's Stone",
                     year=1997, authors=[author1])
        book2 = Book(title="Happy Potter and the Chamber of Secrets",
                     year=1998, authors=[author1])
        book3 = Book(title="A Game of Thrones", year=1996, authors=[author2])
        book4 = Book(title="A Clash of Kings", year=1998, authors=[author2])
        session.add_all([author1, author2, book1, book2, book3, book4])
        session.commit()


@app.get("/authors/", response_model=List[AuthorRead])
def read_authors(session: Session = Depends(get_session)):
    authors = session.exec(select(Author).options(
        selectinload(Author.books))).all()
    return authors


@app.get("/books/", response_model=List[BookRead])
def read_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book).options(
        selectinload(Book.authors))).all()
    return books
