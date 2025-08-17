from fastapi import APIRouter, Query
from app.handlers.hello_handler import HelloHandler
from app.handlers.kindle_handler import KindleHandler
from app.services.kindle_scraper_service import KindleScraperService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

hello_handler = HelloHandler()
kindle_handler = KindleHandler()

@router.get("/hello")
async def get_hello():
    return await hello_handler.get_hello()

@router.get("/kindle/highlights")
def get_kindle_highlights(
    email: str = Query(..., description="Amazon account email"),
    password: str = Query(..., description="Amazon account password")
):
    logger.info(f"Kindle highlights request received for email: {email}")
    return kindle_handler.get_highlights(email, password)