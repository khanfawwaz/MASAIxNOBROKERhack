from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import motor.motor_asyncio
from pymongo import MongoClient
import os

from routers import auth, issues, admin
from database import get_database

# MongoDB connection
MONGO_URL = os.getenv("MONGODB_URL", "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City")
DATABASE_NAME = os.getenv("DATABASE_NAME", "citizen_issue_tracker")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
    app.mongodb = app.mongodb_client[DATABASE_NAME]
    yield
    # Shutdown
    app.mongodb_client.close()

app = FastAPI(
    title="Citizen Issue Tracker API",
    description="A comprehensive API for tracking and managing citizen-reported issues",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Citizen Issue Tracker API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
