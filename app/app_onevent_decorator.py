# @app.on_event decorator is deprecated
# use lifespan event handler instead

# from fastapi import FastAPI

# app = FastAPI()


# @app.on_event("startup")
# async def on_startup():
#     # create_db_and_tables()
#     print("App is starting up...")


# @app.on_event("shutdown")
# async def on_shutdown():
#     print("App is shutting down")


from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App is starting up...")
    yield
    print("App is shutting down...")


app = FastAPI(lifespan=lifespan)

# yields control back to the application in between startup and shutdown
