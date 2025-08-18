from pydantic import BaseModel
from typing import List, Optional

class Highlight(BaseModel):
    book_title: str
    highlight_text: str
    location: Optional[str] = None
    note: Optional[str] = None
