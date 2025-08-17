from fastapi import APIRouter
from app.handlers.hello_handler import HelloHandler

router = APIRouter()

hello_handler = HelloHandler()

@router.get("/hello")
async def get_hello():
    return await hello_handler.get_hello()