# app/main.py
from fastapi import FastAPI, BackgroundTasks
from app.scraper import Scraper
from app.emailer import notify_new_listings
from app.scheduler import start_scheduler

app = FastAPI()

# Database configuration
DB_URI = "mongodb://localhost:27017"
DB_NAME = "real_estate"
COLLECTION_NAME = "listings"

# Email configuration
EMAIL_CONFIG = {
    "to_email": "to@example.com",
    "from_email": "from@example.com",
    "smtp_server": "smtp.example.com",
    "smtp_port": 587,
    "smtp_user": "smtp_user",
    "smtp_password": "smtp_password"
}

scraper = Scraper(db_uri=DB_URI, db_name=DB_NAME, collection_name=COLLECTION_NAME)

@app.on_event("startup")
async def startup_event():
    # Start the background scheduler
    start_scheduler(scraper, EMAIL_CONFIG, interval=3600)  # Run every hour

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Real Estate Scraper API"}

@app.get("/scrape")
async def manual_scrape(background_tasks: BackgroundTasks):
    new_listings = scraper.update_listings()
    background_tasks.add_task(notify_new_listings, new_listings, **EMAIL_CONFIG)
    return {"message": "Scraping started", "new_listings_count": len(new_listings)}

@app.get("/listings")
async def get_listings():
    return scraper.get_all_data_from_db()
