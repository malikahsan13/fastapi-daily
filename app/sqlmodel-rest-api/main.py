from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import Book
from contextlib import asynccontextmanager
from typing import Optional, List

# initialize the database and create tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform startup tasks
    create_db_and_tables()

    yield  # The app is now "running" and handling requests

    # --- SHUTDOWN ---
    # print("Disconnecting from Database...")
    # db_connection.close()


app = FastAPI(lifespan=lifespan)

# Dependency to get a new database session per request


def get_session():
    with Session(engine) as session:
        yield session

# create new book


@app.post("/books/", response_model=Book)
def create_book(book: Book, session: Session = Depends(get_session)):
    session.add(book)
    session.commit()
    # refresh to get the updated instance with generated id
    session.refresh(book)
    return book


@app.get("/books/", response_mode=List[Book])
def read_books(session: Session = Depends(get_session)):
    statement = select(Book)
    results = session.exec(statement)
    return results.all()


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book, session: Session = Depends(get_session)):
    book = session(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    book.title = updated_book.title
    book.author = updated_book.author
    book.description = updated_book.description
    book.year = updated_book.year

    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
    book = session(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}
