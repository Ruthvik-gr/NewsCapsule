from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class NewsModel(BaseModel):
    title: str
    source: str
    media: str
    timestamp: datetime
    finetuned:str
