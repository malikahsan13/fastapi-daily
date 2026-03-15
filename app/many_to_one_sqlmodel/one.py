from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from sqlalchemy.orm import selectinload
from models import Publisher, Book
from schemas import PublisherRead, BookRead
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine


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
        # Check if there are any publishers already
        if not session.exec(select(Publisher)).first():
            # insert dummy publisher with books
            publisher1 = Publisher(
                name="Penguin Books",
                books=[
                    Book(title="Book One", year=2001),
                    Book(title="Book Two", year=2004)
                ]
            )
            publisher2 = Publisher(
                name="HarperCollins",
                books=[
                    Book(title="Book Three", year=2005),
                    Book(title="Book Four", year=2007)
                ]
            )

            session.add([publisher1, publisher2])
            session.commit()
