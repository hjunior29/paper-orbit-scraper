from fastapi import APIRouter, Query
from app.handlers.hello_handler import HelloHandler
from app.handlers.kindle_handler import KindleHandler

router = APIRouter()

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
    return kindle_handler.get_highlights(email, password)