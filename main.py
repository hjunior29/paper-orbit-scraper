from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from src import routes
from config.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Paper Orbit Scraper", version="1.0.0")

app.include_router(routes.router)

if __name__ == "__main__":
    import uvicorn
    import os
    
    log_level = os.getenv("LOG_LEVEL", "INFO").lower()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level=log_level)