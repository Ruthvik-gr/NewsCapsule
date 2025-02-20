from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import pytz
from fastapi import APIRouter
from dotenv import load_dotenv
from src.mongodb.database import news_collection

load_dotenv()

app = FastAPI()

router = APIRouter()

@router.get("/delete-news")
@router.delete("/delete-news")
async def delete_old_news():
    try:
        # Calculate the threshold timestamp (2 days ago)
        two_days_ago = datetime.utcnow() - timedelta(days=2)
        two_days_ago = two_days_ago.replace(tzinfo=pytz.UTC)

        # Fetch old documents before deletion for debugging
        old_documents = await news_collection.find(
            {"timestamp": {"$lt": two_days_ago}}
        ).to_list(length=100)

        if not old_documents:
            return {"message": "No old news articles to delete"}

        # Debugging: Print each document before deletion
        print("Documents to be deleted:")
        for doc in old_documents:
            print(doc)

        # Delete the old documents
        result = await news_collection.delete_many({"timestamp": {"$lt": two_days_ago}})

        return {"message": f"Deleted {result.deleted_count} old news articles"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
