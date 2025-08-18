from app.services.kindle_scraper_service import KindleScraperService
from app.services.crypto_service import CryptoService
import logging
import urllib.parse

from app.utils.response import create_response

logger = logging.getLogger(__name__)

class KindleHandler:
    def __init__(self):
        self.kindle_scraper_service = KindleScraperService(headless=False)
        self.crypto_service = CryptoService()

    def get_highlights(self, encrypted: str, email: str, password: str, headless: str = None):
        logger.info(f"Highlights request received")

        if headless is None:
            headless = "True"
            logger.info(f"Using default headless: {headless}")

        if headless not in ["True", "False"]:
            logger.warning(f"Invalid 'headless' parameter: {headless}")
            return create_response(
                code=400,
                message="Param 'headless' must be 'True' or 'False'",
                data=None
            )

        if encrypted:
            logger.info(f"Processing highlights for encrypted data")
            try:
                encrypted_decoded = urllib.parse.unquote(encrypted)
                logger.info(f"Decoded key: {encrypted_decoded[:20]}...")
                
                credentials = self.crypto_service.decrypt_credentials(encrypted_decoded)
                email = credentials['email']
                password = credentials['password']
            except Exception as e:
                logger.error(f"Error decrypting credentials: {e}")
                return create_response(
                    code=401,
                    message="Invalid encrypted credentials",
                    data=None
                )
        elif not email or not password:
            logger.warning("Required parameters missing")
            return create_response(
                code=401,
                message="Missing required parameters: email and password or encrypted credentials",
                data=None
            )

        logger.info(f"Executando scraper para email: {email[:3]}***")
        
        headless_bool = headless == "True"
        logger.info(f"Headless mode: {headless_bool}")
        
        try:
            scraper = KindleScraperService(headless=headless_bool)
            return scraper.get_highlights(email, password)
        except Exception as e:
            logger.error(f"Error getting highlights: {e}")
            return create_response(
                code=500,
                message="Error retrieving highlights",
                data=None
            )
