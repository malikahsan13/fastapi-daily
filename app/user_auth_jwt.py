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


# Endpoint for user login and token generation
@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=UserOut)
async def get_current_user(token: str = Depends(oauth2_scheme)):

    user_id = validate_token_and_extract_user_id(token)
    print(user_id)

    user = crud.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


def validate_token_and_extract_user_id(token: str) -> int:
    try:
        print(token)
        decoded_token = jwt.decode(
            token, "your-secret-key", algorithms=["HS256"])
        user_id = decoded_token.get("sub")
        print(decoded_token)
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
