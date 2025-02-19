from fastapi import APIRouter
import feedparser
from datetime import datetime
from src.mongodb.models import NewsModel  
from src.mongodb.database import news_collection
from dotenv import load_dotenv
import os
from starlette.responses import StreamingResponse

load_dotenv()

RSS_URL = os.environ["RSS_URL"]

router = APIRouter()



async def fetch_and_store_news():
    """Fetch RSS feed data and store it in MongoDB"""
    print("🔄 Fetching RSS news feed...")
    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        news_data = NewsModel(  # ✅ Use Pydantic model
            title=entry.title,
            source=entry.link,
            description=entry.summary,
            media=entry.media_content[0]["url"] if "media_content" in entry else None,
            timestamp=datetime.utcnow(),
            finetuned="n",
        )

        # Insert into MongoDB if the title does not already exist
        existing = await news_collection.find_one({"title": news_data.title})
        if not existing:
            await news_collection.insert_one(news_data.model_dump())
            print(f"✅ Stored: {news_data.title}")
        else:
            print(f"⚠️ Skipped (Already Exists): {news_data.title}")
    print("fetching completed......................")

async def event_generator():
    yield "News fetching started\n"
    await fetch_and_store_news()  # Run the function
    yield "News fetching ended\n"

@router.get("/fetch-news/")
async def trigger_news_fetch():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
