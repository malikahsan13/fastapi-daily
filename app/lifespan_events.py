from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan():
    # startup code
    print("Application startup: Initialize resource")
    # You can initialize resources here e.g. database connections
    # This point represent the running application (Basically pause the app)
    yield
    # shutdown code
    print("Application shutdown: Cleanup resources")
    # You can clean up resources here e.g. closing database connections


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI application with the new lifespan events!"}
