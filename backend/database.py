from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
import os

# MongoDB connection
MONGO_URL = os.getenv("MONGODB_URL", "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City")
DATABASE_NAME = os.getenv("DATABASE_NAME", "citizen_issue_tracker")

# Global database instance
_database = None

async def get_database() -> AsyncIOMotorDatabase:
    global _database
    if _database is None:
        import motor.motor_asyncio
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        _database = client[DATABASE_NAME]
    return _database
