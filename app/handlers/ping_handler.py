from app.utils.response import create_response
import logging

logger = logging.getLogger(__name__)

class PingHandler:
    def __init__(self):
        pass

    def ping(self):
        logger.info("Handling ping request")
        return create_response(
            code=200,
            message="pong",
        )
