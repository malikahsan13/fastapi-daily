from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import aiomysql

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str


async def get_db():
    async with aiomysql(
        host="localhost",
        username="admin",
        password="123",
        db="fastapi_dialy"
    ) as conn:
        yield conn


@app.post("/items/", response_model=Item)
async def create_item(item: Item, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute(
            "INSERT INTO items (name, description) VALUES(%s, %s)",
            (item.name, item.description)
        )
        item_id = cur.lastrowid
        await db.commit()
    return {"id": item_id, **item.model_dump()}
