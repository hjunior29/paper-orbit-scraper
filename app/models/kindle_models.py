from pydantic import BaseModel
from typing import List, Optional

class Highlight(BaseModel):
    book_title: str
    highlight_text: str
    location: Optional[str] = None
    note: Optional[str] = None

# class KindleHighlightsResponse(BaseModel):
#     highlights: List[Highlight]
#     total_count: int
#     books_processed: int