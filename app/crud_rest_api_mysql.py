from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import aiomysql

app = FastAPI()


class Item(BaseModel):
    id: int
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
