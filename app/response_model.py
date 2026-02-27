from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: str
    name: str
    
@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    return {"id":item_id, "name":f"Item {item_id}"}
