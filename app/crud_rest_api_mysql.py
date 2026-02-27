from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import aiomysql

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float


async def get_db():
    async with aiomysql.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        db="fastapi_1_db"
    ) as conn:
        yield conn


@app.get("/items/", response_model=List[Item])
async def get_items(db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("SELECT * FROM test_items")
        rows = await cur.fetchall()
        items = []
        for row in rows:
            item = Item(id=row[0], name=row[1], price=row[2])
            items.append(item)
        return items


@app.post("/items/", response_model=Item)
async def create_item(item: Item, db=Depends(get_db)):
    async with db.cursor() as cur:
        await cur.execute("INSERT INTO test_items (name, price) VALUES(%s ,%s)",
                          (item.name, item.price))
        # item.id = cur.lastrowid
        await db.commit()
    return item
