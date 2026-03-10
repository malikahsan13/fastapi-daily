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

# Function to create access token


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOROITHM)
    return encoded_jwt

# Function to verify password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to authenticate user


def authticate_user(db: Session, username: str, password: str):
    user = crud.get_user_by_email(db, email=username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

# Endpoint for user registration


@app.post("/register", response_model=schemas.User)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = pwd_context.hash(user.password)
    return crud.createuser(db=db, user=user)
