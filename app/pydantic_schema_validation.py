from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


@app.get("/items/")
async def create_item(item: Item):
    print("Validation Data", item.model_dump())

    return {"message": "Item created successfully", "data": item.model_dump()}
