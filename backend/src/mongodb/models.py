from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class NewsModel(BaseModel):
    title: str
    source: str
    description: str
    media: str
    timestamp: datetime
