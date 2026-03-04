from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt

app = FastAPI()

db = {}


class UserRegister(BaseModel):
    username: str
    pasword: str


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("urf-8")


@app.post("/register/")
async def register_user(user_data: UserRegister):
    if user_data.username in db:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user_data.password)
    db[user_data.username] = hash_password
    return {"message": "User registered successfully"}


@app.post("/login/")
async def login_user(user_data: UserRegister):
    if user_data.username not in db:
        raise HTTPException(status_code=400, detail="User not found")
    hashed_password = db[user_data.username]
    if not bcrypt.checkpw(user_data.password.encode("utf-8"), hashed_password.encode("utf-8")):
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Login successful"}
