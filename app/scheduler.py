from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.scraper import process_by_config


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(process_by_config, 'date', run_date=None)
    scheduler.add_job(process_by_config, 'interval', minutes=10)
    scheduler.start()
