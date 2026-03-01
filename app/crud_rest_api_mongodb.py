from pymongo import mongo_client
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

uri = "mongodb://localhost:27017/fastapi-db"
client = mongo_client(uri)
database = client.get_databae()


users_collection = database('users')


class User(BaseModel):
    name: str
    age: int


async def get_current_database():
    db = database
    yield db


def insert_user(user_data: User):
    user_dict = user_data.dict()
    result = users_collection.insert_one(user_dict)
    return result.inserted_id
