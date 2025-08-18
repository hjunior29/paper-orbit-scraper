from pydantic import BaseModel
from typing import List, Optional

class Highlight(BaseModel):
    book_title: str
    book_author: List[str]
    highlight_text: str
    date: Optional[str] = None
    location: Optional[str] = None
    note: Optional[str] = None
