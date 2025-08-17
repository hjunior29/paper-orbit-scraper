from playwright.sync_api import sync_playwright
from app.models.kindle_models import Highlight
from app.utils.response import create_response
from typing import Dict, List

class KindleScraperService:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.kindle_notebook_url = "https://read.amazon.com/notebook"
    
    def get_highlights(self, email: str, password: str) -> dict:
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()

                # Go to Amazon login page
                page.goto(self.kindle_notebook_url)

                # Fill in email
                page.fill('input[name="email"]', email)
                page.click('input#continue')

                # Fill in password
                page.fill('input[name="password"]', password)
                page.click('input#signInSubmit')

                # Wait for highlights page to load
                page.wait_for_selector('.kp-notebook-library-each-book')

                # Scrape highlights (basic example: print book titles)
                books = page.query_selector_all('.kp-notebook-library-each-book')
                book_to_title = dict[str, str]()
                for book in books:
                    title = book.query_selector('h2.kp-notebook-searchable')
                    if title:
                        book_to_title[book.inner_text()] = title.inner_text()

                # Iterate over all books, click each, and extract highlights
                all_highlights: List[Highlight] = []
                books_processed = 0
                
                for i, book in enumerate(books):
                    book_title = book_to_title[book.inner_text()]
                    # navigate into each book page (although it's an SPA)
                    book.click()
                    # Wait for highlights to load 
                    page.wait_for_selector('.kp-notebook-highlight')
                    # Get all highlight elements
                    highlights = page.query_selector_all('.kp-notebook-highlight')
                    print(f'found {len(highlights)} for Book {i+1}: {book_title}')
                    
                    for h in highlights:
                        highlight_text = h.inner_text().strip()
                        highlight = Highlight(
                            book_title=book_title,
                            highlight_text=highlight_text,
                            location=None,  # Location info would need additional scraping
                            note=None       # Note info would need additional scraping
                        )
                        all_highlights.append(highlight)
                    
                    books_processed += 1

                browser.close()

                # Create response using Pydantic models
                # response_data = KindleHighlightsResponse(
                #     highlights=all_highlights,
                #     total_count=len(all_highlights),
                #     books_processed=books_processed
                # )

                return create_response(
                    code=200,
                    message="Highlights scraped successfully",
                    data=all_highlights
                )

        except Exception as e:
            return create_response(
                code=500,
                message=f"Error scraping highlights: {str(e)}",
                data=None
            )