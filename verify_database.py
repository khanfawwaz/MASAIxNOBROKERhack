#!/usr/bin/env python3
"""
Database Verification Script
This script verifies that the database is properly set up and accessible
"""

import pymongo
from pymongo import MongoClient
from bson import ObjectId

# MongoDB Atlas connection string
MONGODB_URL = "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City"
DATABASE_NAME = "citizen_issue_tracker"

def verify_database():
    print("Verifying Citizen Issue Tracker Database...")
    print("=" * 50)
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URL)
        client.admin.command('ping')
        print("✅ Connected to MongoDB Atlas successfully!")
        
        db = client[DATABASE_NAME]
        
        # Check collections
        collections = db.list_collection_names()
        print(f"✅ Collections found: {collections}")
        
        # Check users
        user_count = db.users.count_documents({})
        admin_count = db.users.count_documents({"role": "admin"})
        citizen_count = db.users.count_documents({"role": "citizen"})
        
        print(f"✅ Users: {user_count} total")
        print(f"   - Admins: {admin_count}")
        print(f"   - Citizens: {citizen_count}")
        
        # Check issues
        issue_count = db.issues.count_documents({})
        pending_count = db.issues.count_documents({"status": "pending"})
        in_progress_count = db.issues.count_documents({"status": "in_progress"})
        completed_count = db.issues.count_documents({"status": "completed"})
        
        print(f"✅ Issues: {issue_count} total")
        print(f"   - Pending: {pending_count}")
        print(f"   - In Progress: {in_progress_count}")
        print(f"   - Completed: {completed_count}")
        
        # Check issue categories
        categories = db.issues.distinct("category")
        print(f"✅ Issue Categories: {', '.join(categories)}")
        
        # Sample data check
        print("\n📋 Sample Data Preview:")
        
        # Show sample users
        print("\n👥 Sample Users:")
        for user in db.users.find({}, {"email": 1, "name": 1, "role": 1}).limit(3):
            print(f"   - {user['name']} ({user['email']}) - {user['role']}")
        
        # Show sample issues
        print("\n📋 Sample Issues:")
        for issue in db.issues.find({}, {"title": 1, "category": 1, "status": 1, "priority": 1}).limit(3):
            print(f"   - {issue['title']} ({issue['category']}) - {issue['status']} - {issue['priority']}")
        
        # Test queries
        print("\n🔍 Testing Queries:")
        
        # Test user lookup
        admin_user = db.users.find_one({"role": "admin"})
        if admin_user:
            print(f"✅ Admin user found: {admin_user['name']}")
        
        # Test issue lookup
        recent_issue = db.issues.find_one({"status": "pending"})
        if recent_issue:
            print(f"✅ Pending issue found: {recent_issue['title']}")
        
        # Test aggregation
        status_counts = list(db.issues.aggregate([
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]))
        print(f"✅ Status distribution: {status_counts}")
        
        print("\n🎉 Database verification completed successfully!")
        print("The database is properly set up and ready for the application.")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False
    
    finally:
        if 'client' in locals():
            client.close()
            print("Database connection closed")

if __name__ == "__main__":
    verify_database()
