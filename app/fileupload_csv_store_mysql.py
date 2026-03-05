from fastapi import FastAPI, UploadFile, File, HTTPException
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_RUL = "mysql+mysqlconnect://root:Admin123@localhost/mydb"

Base = declarative_base()
