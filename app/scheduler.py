from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .scraper import fetch_new_listings
from .emailer import send_email
import asyncio

scheduler = AsyncIOScheduler()
last_timestamp = 0


async def check_new_listings():
    global last_timestamp
    url = "https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&czk_price_summary_order2=0%7C3000000&locality_district_id=72&locality_region_id=14&per_page=20&tms=1722505898806"
    listings = fetch_new_listings(url)
    new_listings = [listing for listing in listings if listing['time_create'] > last_timestamp]

    if new_listings:
        last_timestamp = max(listing['time_create'] for listing in new_listings)
        for listing in new_listings:
            title = listing.get('name')
            url = listing.get('seo', {}).get('locality')
            await send_email(
                subject="New Listing Alert",
                body=f"Check out this new listing: {title}\n{url}",
                to_email="recipient@example.com"
            )


def start_scheduler():
    scheduler.add_job(check_new_listings, 'interval', minutes=10)
    scheduler.start()
