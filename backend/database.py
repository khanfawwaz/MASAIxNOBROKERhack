from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi import Depends
from main import app

async def get_database() -> AsyncIOMotorDatabase:
    return app.mongodb
