import logging
from fastapi import APIRouter
from app import scraper

router = APIRouter(
    prefix="/test",
)
logger = logging.getLogger(__name__)


@router.get("/rate")
async def test_limiter():
    logger.debug("Rate limited")
    return {"message": "You are being rate limited"}


@router.get("/listings")
async def get_listings():
    logger.debug("Getting listings")
    return scraper.get_existing_listings()
