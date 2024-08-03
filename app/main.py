from fastapi import FastAPI
from .scheduler import start_scheduler

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    start_scheduler()


@app.get("/")
async def read_root():
    return {"message": "Sreality scraper running"}
