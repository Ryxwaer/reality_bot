from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv()

client = MongoClient(os.getenv("DB_URI"))
db = client["sreality"]
estates_collection = db["data"]
config_collection = db["config"]

logger.debug("Connected to the database")
