from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import Book
from contextlib import asynccontextmanager
from typing import Optional, List
