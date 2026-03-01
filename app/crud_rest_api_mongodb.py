from pymongo import MongoClient
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from bson import ObjectId

app = FastAPI()

uri = "mongodb://localhost:27017/fastapi-db"
client = MongoClient(uri)
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


@app.post("/users/")
async def create_user(user_data: User):
    user_id = insert_user(user_data)
    return user_id


@app.get("/users/")
async def get_all_users(db: MongoClient = Depends(get_current_database)):
    users = users_collection.find()
    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    return user_list
