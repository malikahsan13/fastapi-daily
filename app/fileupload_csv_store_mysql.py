from fastapi import FastAPI, UploadFile, File, HTTPException
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnect://root:Admin123@localhost/mydb"

Base = declarative_base()


class Item(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,  index=True)
    name = Column(String)


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


@app.post("/upload-csv/")
