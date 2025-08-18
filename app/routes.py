from fastapi import APIRouter, Query
from app.handlers.kindle_handler import KindleHandler
from app.handlers.ping_handler import PingHandler
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

kindle_handler = KindleHandler()

@router.get("/kindle/highlights")
def get_kindle_highlights(
    encrypted: str = Query(None, description="Use secure endpoint with encrypted credentials"),
    email: str = Query(None, description="Amazon account email"),
    password: str = Query(None, description="Amazon account password"),
    headless: str = Query(None, description="Run browser in headless mode")
):
    return kindle_handler.get_highlights(encrypted, email, password, headless)

@router.get("/ping")
def ping():
    return PingHandler().ping()
