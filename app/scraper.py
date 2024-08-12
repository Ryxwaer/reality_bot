from typing import List
import re
from zoneinfo import ZoneInfo
import requests
import pandas as pd
from datetime import datetime
from app.db.database import estates_collection, config_collection
from app.emailer import Emailer
import logging

emailer = Emailer()
logger = logging.getLogger(__name__)


def extract_urls(id, estate):
    seo = estate.get("seo", {})
    locality = seo.get("locality", "")
    name = estate.get("name", "")
    type = get_type_from_name(name)
    if locality and name and id:
        return f"https://www.sreality.cz/detail/prodej/byt/{type}/{locality}/{id}"
    return ""


def fetch_new_listings(url: str) -> List[dict]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    # throw error
    response.raise_for_status()


def get_type_from_name(name):
    # Targets 1+1, 2+kk and similar patterns
    pattern = r"\b(\d+\+\S+)\b"
    try:
        type = re.findall(pattern, name)[0]
    except IndexError:
        type = "Unknown"
    return type


def fetch_listings(url):
    data = fetch_new_listings(url)
    estates = data["_embedded"]["estates"]
    current_date = datetime.now(ZoneInfo("Europe/Bratislava")).strftime("%Y-%m-%dT%H:%M:%S%z")
    estate_data = []

    for estate in estates:
        id = estate.get("hash_id", "")
        estate_info = {
            "id": id,
            "name": estate["name"],
            "locality": estate["locality"],
            "price": "{:,}".format(estate["price"]).replace(",", " "),
            "features": ', '.join(estate.get("labelsAll", [])[0]),
            "url": extract_urls(id, estate),
            "scraped": current_date,
        }
        estate_data.append(estate_info)

    df_estates = pd.DataFrame(estate_data)
    return df_estates


def get_existing_listings():
    existing_listings = list(estates_collection.find({}, {"_id": 0}))
    df_existing = pd.DataFrame(existing_listings)
    return df_existing


def save_new_listings(new_listings):
    estates_collection.insert_many(new_listings.to_dict('records'))


def scrape_and_compare(config, existing_ids):
    current_listings = fetch_listings(config['url'])

    new_listings = current_listings[~current_listings['id'].isin(existing_ids)] \
        if len(existing_ids) else current_listings

    if new_listings.empty:
        return

    if emailer.send_email(config, new_listings):
        save_new_listings(new_listings)
        logger.info(f"saved {len(new_listings)} newly found listings.")


def process_by_config():
    logger.debug("Processing started")

    existing_listings = get_existing_listings()
    existing_ids = existing_listings['id'].unique()

    configs = config_collection.find({})
    for config in configs:
        scrape_and_compare(config, existing_ids)
    emailer.disconnect()
