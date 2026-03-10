from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, crud, schemas
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from .models import Base
from .schemas import UserOut

app = FastAPI()

# Create all database tables
Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# JWT authentication settings
SECRET_KEY = "your-secret-key"
ALGOROITHM = "H256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Password hasing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated=auto)

# Dependency to get database session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
