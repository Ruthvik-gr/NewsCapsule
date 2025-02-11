from sched import scheduler
from fastapi import APIRouter
import feedparser
from datetime import datetime
from src.mongodb.models import NewsModel  # ✅ Import the Pydantic model
from src.mongodb.database import news_collection  # ✅ Import MongoDB collection

router = APIRouter()
RSS_URL = "https://www.firstpost.com/commonfeeds/v1/mfp/rss/health.xml"

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
            finetuned="n"
        )

        # Insert into MongoDB if the title does not already exist
        existing = await news_collection.find_one({"title": news_data.title})
        if not existing:
            await news_collection.insert_one(news_data.model_dump()) 
            print(f"✅ Stored: {news_data.title}")
        else:
            print(f"⚠️ Skipped (Already Exists): {news_data.title}")

@router.get("/fetch-news/")
async def trigger_news_fetch():
    """Manually trigger fetching and storing news"""
    await fetch_and_store_news()
    return {"message": "News fetching started"}


def shutdown():
    """Shutdown function for scheduler"""
    scheduler.shutdown()
