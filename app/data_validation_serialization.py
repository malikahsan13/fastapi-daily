from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field, EmailStr, validator
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel, Session, select
from typing import List
from contextlib import asynccontextmanager
from database import create_db_and_tables, engine

class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=100)

    @validator('name')
    def validate_names(cls, v):
        if not v.isalpa():
            raise ValueError("Name must contain only alphabetic characters")
        return v

# SQLModel model for the database
class User(SQLModel, table= True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., min_length=3, max_length=50)
    email: str
    age: int = Field(..., ge=18, le=100)

@asynccontextmanager
async def lifespan():
    create_db_and_tables(app: FastAPI)
    yield
    
app = FastAPI(lifespan=lifespan)

def get_session():
    with Session(engine) as session:
        yield session
    
    
# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract and format only the error message
    error_messages = [err['msg'] for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"errors": error_messages}
        
    )
    
# Custom exception handler for other HTTP exceptions
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail":exc.detail}
    )
    
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User(name = user.name, email = user.email, age = user.age)
    try:
        session.add(db_user)
        session.commit()
        session.refresh()
        return db_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
