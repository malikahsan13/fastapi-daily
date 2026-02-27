from fastapi import FastAPI, Depends

app = FastAPI()

def get_db_connection():
    return "Fake DB Connection"

def get_current_user():
    return "Fake user"

@app.get("/items")
async def read_items(db: str = Depends(get_db_connection), current_user: str = Depends(get_current_user)):
    return {"db_connection": db, "current_user": current_user}