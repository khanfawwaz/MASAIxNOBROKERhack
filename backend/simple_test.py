#!/usr/bin/env python3
"""
Simple MongoDB connection test
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongodb_connection():
    """Test MongoDB connection"""
    try:
        # MongoDB Atlas connection string
        mongodb_url = "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City"
        database_name = "citizen_issue_tracker"
        
        print(f"🔗 Connecting to MongoDB Atlas...")
        print(f"Database: {database_name}")
        
        # Create MongoDB client
        client = AsyncIOMotorClient(mongodb_url)
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Get database
        db = client[database_name]
        
        # Test database operations
        print(f"📊 Testing database operations...")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"Collections: {collections}")
        
        # Test insert operation
        test_collection = db.test_connection
        test_doc = {"test": "connection", "timestamp": "2024-01-01"}
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Test find operation
        found_doc = await test_collection.find_one({"_id": result.inserted_id})
        print(f"✅ Test document found: {found_doc}")
        
        # Clean up test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        # Close connection
        client.close()
        print("✅ MongoDB connection test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Testing MongoDB Atlas Connection")
    print("=" * 40)
    
    # Run the test
    success = asyncio.run(test_mongodb_connection())
    
    if success:
        print("\n🎉 MongoDB Atlas setup is complete and working!")
        print("You can now start the application with: npm run dev")
    else:
        print("\n❌ MongoDB Atlas setup failed. Please check your connection string and try again.")
        print("Make sure your MongoDB Atlas cluster is running and accessible.")
