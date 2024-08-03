# app/scraper.py
import requests
import pymongo
from datetime import datetime
from typing import List, Dict

class Scraper:
    def __init__(self, db_uri: str, db_name: str, collection_name: str):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def fetch_data_from_api(self) -> List[Dict]:
        url = "https://www.sreality.cz/api/v2/estates"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["_embedded"]["estates"]
        else:
            response.raise_for_status()

    def get_all_data_from_db(self) -> List[Dict]:
        return list(self.collection.find())

    def get_new_listings(self) -> List[Dict]:
        api_data = self.fetch_data_from_api()
        db_data = self.get_all_data_from_db()

        db_ids = {item["hash_id"] for item in db_data}
        new_listings = [item for item in api_data if item["hash_id"] not in db_ids]

        return new_listings

    def store_new_listings(self, listings: List[Dict]):
        if listings:
            for listing in listings:
                listing["scraped_at"] = datetime.utcnow()
            self.collection.insert_many(listings)

    def update_listings(self):
        new_listings = self.get_new_listings()
        self.store_new_listings(new_listings)
        return new_listings
app/scheduler.py