# from sched import scheduler
# from fastapi import APIRouter
# import feedparser
# from datetime import datetime
# from src.mongodb.models import NewsModel  # ✅ Import the Pydantic model
# from src.mongodb.database import news_collection  # ✅ Import MongoDB collection
# from dotenv import load_dotenv
# import os
# load_dotenv()

# RSS_URL = os.environ["RSS_URL"]

# router = APIRouter()
# async def fetch_and_store_news():
#     """Fetch RSS feed data and store it in MongoDB"""
#     print("🔄 Fetching RSS news feed...")
#     feed = feedparser.parse(RSS_URL)

#     for entry in feed.entries:
#         news_data = NewsModel(  # ✅ Use Pydantic model
#             title=entry.title,
#             source=entry.link,
#             description=entry.summary,
#             media=entry.media_content[0]["url"] if "media_content" in entry else None,
#             timestamp=datetime.utcnow(),
#             finetuned="n"
#         )

#         # Insert into MongoDB if the title does not already exist
#         existing = await news_collection.find_one({"title": news_data.title})
#         if not existing:
#             await news_collection.insert_one(news_data.model_dump()) 
#             print(f"✅ Stored: {news_data.title}")
#         else:
#             print(f"⚠️ Skipped (Already Exists): {news_data.title}")

# @router.get("/fetch-news/")
# async def trigger_news_fetch():
#     """Manually trigger fetching and storing news"""
#     await fetch_and_store_news()
#     return {"message": "News fetching started"}


# def shutdown():
#     """Shutdown function for scheduler"""
#     scheduler.shutdown()






from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import APIRouter
import feedparser
from datetime import datetime
from src.mongodb.models import NewsModel  # ✅ Import the Pydantic model
from src.mongodb.database import news_collection  # ✅ Import MongoDB collection
from dotenv import load_dotenv
import os
import asyncio
load_dotenv()

RSS_URL = os.environ["RSS_URL"]

router = APIRouter()

scheduler = BackgroundScheduler()

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
    print("fetching completed......................")
    
# Wrapper to call async function in scheduler
def call_fetch_and_store_news():
    asyncio.run(fetch_and_store_news())


# Schedule the task to run every day at 6:00 AM
scheduler.add_job(
    call_fetch_and_store_news,  # Call the sync wrapper instead of the async function directly
    CronTrigger(hour=18, minute=43),  # Run at 6:00 AM every day
    id="daily_news_fetch",
    replace_existing=True
)

# Start the scheduler
scheduler.start()

def shutdown():
    """Shutdown function for scheduler"""
    scheduler.shutdown()
