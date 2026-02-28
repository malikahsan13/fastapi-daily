from pymongo import MongoClient
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

uri = "mongodb://localhost:27017/fastapi-db"
client = MongoClient(uri)
database = client.get_database()  # removed db name since it is reterived from uri

users_collection = database['users']


class User(BaseModel):
    name: str
    age: int


async def get_current_database():
    db = database
    yield db


def insert_user(user_data):
    user_dict = user_data.dict()  # convert pydantic model to dict
    result = users_collection.insert_one(user_dict)
    return result.inserted_id


@app.post("/users/")
async def create_user(user_data: User):
    user_id = insert_user(user_data)
    return {"message": "User created successfully", "user_id": str(user_id)}
