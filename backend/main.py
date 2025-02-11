from fastapi import FastAPI
from src.mongodb.database import connect_db
from src.routes.fetchnews import router as news_router  
from src.routes.fetchnews import shutdown 
from contextlib import asynccontextmanager 

app = FastAPI(
    title="News Agent app",
    summary="A Simple application to get the rss feed and fine tune it withh llm's and show a short.",
)


@app.get("/")
async def root():
    return await connect_db()


# Include the news routes
app.include_router(news_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown"""
    yield  # Application runs here
    shutdown()  # Cleanup when FastAPI stops