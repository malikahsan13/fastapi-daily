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
