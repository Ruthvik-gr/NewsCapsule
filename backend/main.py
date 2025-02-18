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


# @app.get("/")
# async def root():
#     try:
#         return await connect_db()  # Attempt to connect to the database
#     except Exception as e:
#         # If connection fails, catch the error and return a helpful message
#         return {"error": f"Failed to connect to MongoDB: {str(e)}"}


@app.get("/test-db")
async def test_db():
    try:
        # Try to ping the database
        await client.admin.command('ping')
        return {"message": "MongoDB connection is successful"}
    except Exception as e:
        return {"error": f"Failed to connect to MongoDB: {str(e)}"}


# Include the news routes
app.include_router(news_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    yield  # Application runs here
    shutdown()  # Cleanup when FastAPI stops
