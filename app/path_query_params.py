from fastapi import FastAPI

app = FastAPI()

# path param


@app.get("/items/{item_id}")
async def read_items(item_id: int):
    return {"item_id": item_id}


# query param
@app.get("/items/")
async def read_item2(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
