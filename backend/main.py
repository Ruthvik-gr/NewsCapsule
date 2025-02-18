from fastapi import FastAPI
from src.mongodb.database import connect_db
from src.mongodb.database import client
from src.routes.fetchnews import router as news_router
from src.routes.fetchnews import shutdown
from contextlib import asynccontextmanager

app = FastAPI(
    title="News Agent app",
    summary="A Simple application to get the rss feed and fine tune it withh llm's and show a short.",
)


@app.get("/")
async def root():
    print("Root endpoint hit")
    result = await connect_db()
    print(f"MongoDB connection result: {result}")
    return result


# Include the news routes
app.include_router(news_router)


# c
