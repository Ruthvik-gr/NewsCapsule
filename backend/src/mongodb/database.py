from fastapi import FastAPI
import motor.motor_asyncio
from dotenv import load_dotenv
import os
load_dotenv()

MONGO_URI = os.environ["MONGODB_URL"]
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.newsapp
news_collection = db.get_collection("news_collection")

# Function to initialize the database connection
async def connect_db():
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB successfully!")
        return {"message": "FastAPI with MongoDB is working! ✅"}
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")