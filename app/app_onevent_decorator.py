# @app.on_event decorator is deprecated
# use lifespan event handler instead

from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    # create_db_and_tables()
    print("App is starting up...")


@app.on_event("shutdown")
async def on_shutdown():
    print("App is shutting down")
