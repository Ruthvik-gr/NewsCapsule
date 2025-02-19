from fastapi import FastAPI
from src.mongodb.database import connect_db
from src.routes.fetchnews import router as news_router
from contextlib import asynccontextmanager
from src.routes.process_news import router as processrouter

app = FastAPI(
    title="News Agent app",
    summary="A Simple application to get the rss feed and fine tune it withh llm's and show a short.",
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!"}


@app.get("/testdb")
async def root():
    try:
        return await connect_db()  # Attempt to connect to the database
    except Exception as e:
        # If connection fails, catch the error and return a helpful message
        return {"error": f"Failed to connect to MongoDB: {str(e)}"}


# Include the news routes
app.include_router(news_router)
app.include_router(processrouter)
