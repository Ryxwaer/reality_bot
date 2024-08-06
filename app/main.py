import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers import test
from app.scheduler import start_scheduler
from .logging_config import setup_logging

load_dotenv()
setup_logging()

app = FastAPI()

app.include_router(test.router)


@app.on_event("startup")
async def startup_event():
    logging.info("Starting the scheduler")
    start_scheduler()


@app.get("/")
async def read_root():
    return {"message": "Welcome to the SReality scraper API"}
