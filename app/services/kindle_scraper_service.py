from playwright.sync_api import sync_playwright
from app.models.kindle_models import Highlight
from app.utils.response import create_response
from app.utils.scraper import human_type, human_click
from typing import List
import random
import time
import logging

logger = logging.getLogger(__name__)

class KindleScraperService:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.kindle_notebook_url = "https://read.amazon.com/notebook"
        logger.info(f"KindleScraperService initialized with headless={headless}")
    
    def get_highlights(self, email: str, password: str) -> dict:
        logger.info("Starting highlights scraping process")
        
        try:
            with sync_playwright() as p:
                logger.debug("Launching browser")
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()
                logger.debug("Browser and page created successfully")

                logger.info(f"Navigating to {self.kindle_notebook_url}")
                page.goto(self.kindle_notebook_url)
                logger.debug("Login page loaded")

                logger.info("Filling email field")
                email_input = page.locator('input[name="email"]')
                human_type(email_input, email)
                
                delay = random.uniform(1, 2)
                logger.debug(f"Waiting {delay:.2f}s before clicking continue")
                time.sleep(delay)
                page.click('input#continue')
                logger.debug("Continue button clicked")

                logger.info("Filling password field")
                password_input = page.locator('input[name="password"]')
                human_type(password_input, password)
                
                delay = random.uniform(1, 2)
                logger.debug(f"Waiting {delay:.2f}s before clicking sign in")
                time.sleep(delay)
                page.click('input#signInSubmit')
                logger.debug("Sign in button clicked")

                logger.info("Waiting for highlights page to load")
                page.wait_for_selector('.kp-notebook-library-each-book')
                logger.debug("Highlights page loaded successfully")

                books = page.query_selector_all('.kp-notebook-library-each-book')
                logger.info(f"Found {len(books)} books in library")
                
                book_to_title = dict[str, str]()
                for book in books:
                    title = book.query_selector('h2.kp-notebook-searchable')
                    if title:
                        book_to_title[book.inner_text()] = title.inner_text()
                
                logger.debug(f"Mapped {len(book_to_title)} book titles")

                logger.info("Starting to process books for highlights extraction")
                all_highlights: List[Highlight] = []
                books_processed = 0
                
                for i, book in enumerate(books):
                    book_title = book_to_title[book.inner_text()]
                    logger.info(f"Processing book {i+1}/{len(books)}: {book_title}")
                    
                    delay = random.uniform(0.5, 1.5)
                    logger.debug(f"Waiting {delay:.2f}s before clicking book")
                    time.sleep(delay)
                    human_click(page, book)
                    
                    logger.debug("Waiting for highlights to load")
                    page.wait_for_selector('.kp-notebook-highlight')
                    
                    delay = random.uniform(0.3, 0.8)
                    logger.debug(f"Waiting {delay:.2f}s after highlights loaded")
                    time.sleep(delay)
                    
                    highlights = page.query_selector_all('.kp-notebook-highlight')
                    logger.info(f'Found {len(highlights)} highlights for book: {book_title}')
                    
                    for j, h in enumerate(highlights):
                        highlight_text = h.inner_text().strip()
                        highlight = Highlight(
                            book_title=book_title,
                            highlight_text=highlight_text,
                            location=None,  # Location info would need additional scraping
                            note=None       # Note info would need additional scraping
                        )
                        all_highlights.append(highlight)
                        logger.debug(f"Processed highlight {j+1}/{len(highlights)} from {book_title}")
                    
                    books_processed += 1
                    logger.info(f"Completed processing book {i+1}: {book_title} ({len(highlights)} highlights)")

                logger.debug("Closing browser")
                browser.close()
                
                logger.info(f"Scraping completed successfully. Total highlights: {len(all_highlights)} from {books_processed} books")
                return create_response(
                    code=200,
                    message="Highlights scraped successfully",
                    data=[highlight.model_dump() for highlight in all_highlights]
                )

        except Exception as e:
            logger.error(f"Error during highlights scraping: {str(e)}", exc_info=True)
            return create_response(
                code=500,
                message=f"Error scraping highlights: {str(e)}",
                data=None
            )
    
