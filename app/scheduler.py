# app/scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scraper import Scraper
from app.emailer import notify_new_listings

def start_scheduler(scraper: Scraper, email_config: Dict, interval: int):
    scheduler = AsyncIOScheduler()

    def job():
        new_listings = scraper.update_listings()
        notify_new_listings(new_listings, **email_config)

    scheduler.add_job(job, 'interval', seconds=interval)
    scheduler.start()
