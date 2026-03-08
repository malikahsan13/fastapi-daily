from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler

app = FastAPI()

# Initialize the scheduler
scheduler = AsyncIOScheduler()


async def my_task():
    print("Executing my task")


@app.on_event("startup")
async def start_scheduler():
    scheduler.add_job(my_task, "interval", seconds=10)
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}
