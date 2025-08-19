from pydantic import BaseModel
from typing import List, Optional

class HighlightItem(BaseModel):
    text: str
    note: Optional[str] = None

class Highlight(BaseModel):
    book_title: str
    book_author: List[str]
    book_cover: Optional[str] = None
    highlights: List[HighlightItem]
    date: Optional[str] = None
