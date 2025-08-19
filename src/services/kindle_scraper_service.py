from playwright.sync_api import sync_playwright
from src.models.kindle_models import Highlight, HighlightItem
from src.utils.response import create_response
from src.utils.scraper import human_type, human_click
from typing import List, Optional
import random
import time
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class KindleScraperService:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.kindle_notebook_url = "https://read.amazon.com/notebook"
        self.puzzle_selectors = [
            'text=puzzle',
            'text=/puzzle/i',
            'text="Solve this puzzle"',
            'text="Authentication required"',
            'iframe[title*="verification"]',
            'iframe[title*="puzzle"]',
            '.cvf-widget-container',
            '#cvf-aamation-challenge-iframe'
        ]
        logger.info(f"KindleScraperService initialized with headless={headless}")
    
    def _parse_authors(self, author_text: str) -> List[str]:
        """Parse author text and split by common delimiters"""
        if not author_text:
            return ["Unknown Author"]
        
        # Remove "By: " prefix if present
        if author_text.startswith("By: "):
            author_text = author_text[4:]
        
        # Split by common delimiters and clean up
        authors = re.split(r',|\band\b', author_text, flags=re.IGNORECASE)
        authors = [author.strip() for author in authors if author.strip()]
        
        return authors if authors else ["Unknown Author"]
    
    def _parse_date(self, date_input: str) -> Optional[str]:
        """Parse date from input field value and convert to mm-dd-yyyy format
        
        Args:
            date_input: Expected format like "Sunday August 17, 2025" or "August 17, 2025"
            
        Returns:
            Formatted date string in mm-dd-yyyy format or None if parsing fails
        """
        if not date_input:
            return None
        
        try:
            date_parts = date_input.split(maxsplit=1)
            if len(date_parts) > 1:
                date_str = date_parts[1]
            else:
                date_str = date_input
            
            parsed_date = datetime.strptime(date_str, "%B %d, %Y")
            
            return parsed_date.strftime("%m-%d-%Y")
        except ValueError:
            logger.warning(f"Could not parse date: {date_input}")
            return None
    
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
                
                try:
                    for selector in self.puzzle_selectors:
                        try:
                            puzzle_element = page.wait_for_selector(selector, timeout=1000)
                            if puzzle_element:
                                logger.error(f"Puzzle/captcha detected with selector: {selector}")
                                browser.close()
                                return create_response(
                                    code=400,
                                    message="Authentication blocked by puzzle/captcha. Please try again later.",
                                    data=None
                                )
                        except:
                            continue
                except:
                    # No puzzle found, continue normally
                    pass
                
                page.wait_for_selector('.kp-notebook-library-each-book')
                logger.debug("Highlights page loaded successfully")

                books = page.query_selector_all('.kp-notebook-library-each-book')
                logger.info(f"Found {len(books)} books in library")
                
                # Extract book info with unique IDs
                book_data = []
                for book in books:
                    book_id = book.get_attribute('id')
                    title_elem = book.query_selector('h2.kp-notebook-searchable')
                    author_elem = book.query_selector('p.a-spacing-base.a-color-secondary')
                    cover_elem = book.query_selector('img.kp-notebook-cover-image')
                    
                    if title_elem and book_id:
                        title = title_elem.inner_text()
                        authors = ["Unknown Author"]
                        if author_elem:
                            author_text = author_elem.inner_text().strip()
                            authors = self._parse_authors(author_text)
                        
                        cover_url = None
                        if cover_elem:
                            cover_url = cover_elem.get_attribute('src')
                        
                        book_data.append({
                            'id': book_id,
                            'title': title,
                            'authors': authors,
                            'cover': cover_url
                        })
                
                logger.debug(f"Mapped {len(book_data)} book titles")

                logger.info("Starting to process books for highlights extraction")
                all_books_highlights: List[Highlight] = []
                books_processed = 0
                
                for i, book_info in enumerate(book_data):
                    book_id = book_info['id']
                    book_title = book_info['title']
                    book_authors = book_info['authors']
                    book_cover = book_info['cover']
                    authors_str = ", ".join(book_authors)
                    logger.info(f"Processing book {i+1}/{len(book_data)}: {book_title} by {authors_str}")
                    
                    page.evaluate(f"""
                        const book = document.querySelector('#{book_id}');
                        const scroller = document.querySelector('.a-scroller.kp-notebook-scroller-addon.a-scroller-vertical');
                        if (book && scroller) {{
                            const bookRect = book.getBoundingClientRect();
                            const scrollerRect = scroller.getBoundingClientRect();
                            const offset = bookRect.top - scrollerRect.top + scroller.scrollTop - 50;
                            scroller.scrollTop = Math.max(0, offset);
                        }}
                    """)
                    
                    time.sleep(random.uniform(0.3, 0.8))
                    
                    action_selector = f'#{book_id} span[data-action="get-annotations-for-asin"]'
                    action_element = page.query_selector(action_selector)
                    if action_element:
                        delay = random.uniform(0.5, 1.5)
                        logger.debug(f"Waiting {delay:.2f}s before clicking book action span")
                        time.sleep(delay)
                        human_click(page, action_element)
                        clicked = True
                        logger.debug(f"Successfully clicked action span for {book_id}")
                    else:
                        book_element = page.query_selector(f'#{book_id}')
                        if book_element:
                            delay = random.uniform(0.5, 1.5)
                            time.sleep(delay)
                            human_click(page, book_element)
                            clicked = True
                            logger.debug(f"Successfully clicked book container for {book_id}")
                    
                    if not clicked:
                        logger.warning(f"Could not find any clickable element for book {book_id}")
                        continue
                    
                    logger.debug("Waiting for highlights to load")
                    page.wait_for_selector('.kp-notebook-highlight')
                    
                    delay = random.uniform(0.3, 0.8)
                    logger.debug(f"Waiting {delay:.2f}s after highlights loaded")
                    time.sleep(delay)
                    
                    highlight_containers = page.query_selector_all('.a-row.a-spacing-base')
                    logger.info(f'Found {len(highlight_containers)} highlight containers for book: {book_title}')
                    
                    date_span = page.query_selector('span#kp-notebook-annotated-date')
                    highlight_date = None
                    if date_span:
                        date_text = date_span.inner_text().strip()
                        highlight_date = self._parse_date(date_text)
                        logger.debug(f"Extracted date: {date_text} -> {highlight_date}")
                    
                    book_highlights = []
                    for container in highlight_containers:
                        # Extract highlight text
                        highlight_elem = container.query_selector('.kp-notebook-highlight')
                        if not highlight_elem:
                            continue
                            
                        highlight_text = highlight_elem.inner_text().strip()
                        
                        # Extract note if present
                        note_elem = container.query_selector('.kp-notebook-note span#note')
                        note_text = None
                        if note_elem:
                            note_text = note_elem.inner_text().strip()
                            if not note_text:
                                note_text = None
                        
                        book_highlights.append(HighlightItem(
                            text=highlight_text,
                            note=note_text
                        ))
                    
                    if book_highlights:
                        book_highlight = Highlight(
                            book_title=book_title,
                            book_author=book_authors,
                            book_cover=book_cover,
                            highlights=book_highlights,
                            date=highlight_date
                        )
                        all_books_highlights.append(book_highlight)
                    
                    books_processed += 1
                    logger.info(f"Completed processing book {i+1}: {book_title} ({len(book_highlights)} highlights)")
                    

                logger.debug("Closing browser")
                browser.close()
                
                total_highlights = sum(len(book.highlights) for book in all_books_highlights)
                logger.info(f"Scraping completed successfully. Total highlights: {total_highlights} from {books_processed} books")
                return create_response(
                    code=200,
                    message="Highlights scraped successfully",
                    data=[book.model_dump() for book in all_books_highlights]
                )

        except Exception as e:
            logger.error(f"Error during highlights scraping: {str(e)}", exc_info=True)
            return create_response(
                code=500,
                message=f"Error scraping highlights: {str(e)}",
                data=None
            )
    
