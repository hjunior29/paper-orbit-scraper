from app.services.kindle_scraper_service import KindleScraperService

class KindleHandler:
    def __init__(self):
        self.kindle_scraper_service = KindleScraperService(headless=False)  # Visível por padrão
    
    def get_highlights(self, email: str, password: str, headless: bool = False):
        if headless != self.kindle_scraper_service.headless:
            scraper = KindleScraperService(headless=headless)
            return scraper.get_highlights(email, password)
        
        return self.kindle_scraper_service.get_highlights(email, password)