from pymongo import MongoClient
from fastapi import FastAPI, Depends, Path, HTTPException
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
    user_dict = user_data.model_dump()
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


@app.get("/users/{user_id}")
async def get_user(user_id: str = Path(...), db: MongoClient = Depends(get_current_database)):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.put("/user/{user_id}")
async def update_user(user_data: User, user_id: str = Path(...), db: MongoClient = Depends(get_current_database)):
    user_dict = user_data.model_dump()
    user_object_id = ObjectId(user_id)
    result = users_collection.find_one(
        {"_id": user_object_id}, {"$set": user_dict})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: str = Path(...), db: MongoClient = Depends(get_current_database)):
    user_object_id = ObjectId(user_id)
    result = users_collection.delete_one({"_id": user_object_id})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
