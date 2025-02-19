from src.langchain.summary import process_url
from src.mongodb.database import news_collection
from starlette.responses import StreamingResponse
from fastapi import APIRouter

router = APIRouter()

async def process_unprocessed_news():
    """Fetch unprocessed news and update them with processed summaries."""
    try:
        cursor = news_collection.find({"finetuned": "n"})
        unprocessed_articles = [article async for article in cursor]

        for article in unprocessed_articles:
            try:
                source_url = article["source"]
                description = process_url(source_url)

                if description:
                    await news_collection.update_one(
                        {"_id": article["_id"]},
                        {"$set": {"summary": description, "finetuned": "y"}},
                    )
                    print(f"✅ Processed article ID: {article['_id']}")
                else:
                    print(f"⚠️ Skipped article {article['_id']} due to invalid description.")

            except Exception as e:
                print(f"❌ Error processing article {article['_id']}: {str(e)}")

    except Exception as e:
        print(f"❌ Database error: {str(e)}")

async def event_generator():
    yield "News process started\n"
    await process_unprocessed_news()  # Run the function
    yield "News process ended\n"

@router.get("/process-news/")
async def trigger_news_fetch():
    return StreamingResponse(event_generator(), media_type="text/event-stream")