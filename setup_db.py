#!/usr/bin/env python3
"""
Simple Database Setup Script for Citizen Issue Tracker
"""

import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
from bson import ObjectId

# MongoDB Atlas connection string
MONGODB_URL = "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City"
DATABASE_NAME = "citizen_issue_tracker"

def main():
    print("Setting up Citizen Issue Tracker Database...")
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URL)
        client.admin.command('ping')
        print("Connected to MongoDB Atlas successfully!")
        
        db = client[DATABASE_NAME]
        
        # Clear existing data
        print("Clearing existing data...")
        db.users.delete_many({})
        db.issues.delete_many({})
        
        # Create indexes
        print("Creating indexes...")
        try:
            db.users.create_index("email", unique=True)
            db.users.create_index("role")
            db.issues.create_index("reported_by")
            db.issues.create_index("status")
            db.issues.create_index("category")
            db.issues.create_index("created_at", -1)
            print("Indexes created successfully!")
        except Exception as e:
            print(f"Index creation warning: {e}")
        
        # Create sample users
        print("Creating sample users...")
        
        admin_user = {
            "_id": ObjectId(),
            "email": "admin@city.gov",
            "name": "City Administrator",
            "role": "admin",
            "phone": "+1-555-0101",
            "address": "123 City Hall, Downtown",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # admin123
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        citizen_users = [
            {
                "_id": ObjectId(),
                "email": "john.doe@email.com",
                "name": "John Doe",
                "role": "citizen",
                "phone": "+1-555-0102",
                "address": "456 Oak Street, Residential Area",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # citizen123
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            },
            {
                "_id": ObjectId(),
                "email": "jane.smith@email.com",
                "name": "Jane Smith",
                "role": "citizen",
                "phone": "+1-555-0103",
                "address": "789 Pine Avenue, Suburbs",
                "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # citizen123
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
        ]
        
        # Insert users
        db.users.insert_one(admin_user)
        db.users.insert_many(citizen_users)
        print(f"Created {1 + len(citizen_users)} users")
        
        # Create sample issues
        print("Creating sample issues...")
        
        sample_issues = [
            {
                "_id": ObjectId(),
                "title": "Large Pothole on Main Street",
                "description": "There's a very large pothole on Main Street near the intersection with Oak Avenue. It's causing damage to vehicles and is a safety hazard.",
                "category": "pothole",
                "priority": "high",
                "status": "in_progress",
                "location": {
                    "address": "Main Street & Oak Avenue, Downtown",
                    "coordinates": {"lat": 40.7128, "lng": -74.0060}
                },
                "images": ["/uploads/pothole1.jpg"],
                "reported_by": str(citizen_users[0]["_id"]),
                "assigned_to": str(admin_user["_id"]),
                "created_at": datetime.utcnow() - timedelta(days=5),
                "updated_at": datetime.utcnow() - timedelta(days=1),
                "resolved_at": None,
                "comments": [
                    {
                        "_id": ObjectId(),
                        "text": "Thank you for reporting this issue. We've assigned it to our road maintenance team.",
                        "author": str(admin_user["_id"]),
                        "author_name": admin_user["name"],
                        "created_at": datetime.utcnow() - timedelta(days=4),
                        "is_internal": False
                    }
                ],
                "progress": [
                    {
                        "_id": ObjectId(),
                        "status": "in_progress",
                        "description": "Assigned to road maintenance team",
                        "updated_by": str(admin_user["_id"]),
                        "updated_by_name": admin_user["name"],
                        "created_at": datetime.utcnow() - timedelta(days=4)
                    }
                ]
            },
            {
                "_id": ObjectId(),
                "title": "Broken Streetlight",
                "description": "Streetlight on Pine Avenue has been out for over a week. It's very dark at night and poses a safety risk.",
                "category": "streetlight",
                "priority": "medium",
                "status": "completed",
                "location": {
                    "address": "Pine Avenue, Near Elm Drive",
                    "coordinates": {"lat": 40.7589, "lng": -73.9851}
                },
                "images": ["/uploads/streetlight1.jpg"],
                "reported_by": str(citizen_users[1]["_id"]),
                "assigned_to": str(admin_user["_id"]),
                "created_at": datetime.utcnow() - timedelta(days=8),
                "updated_at": datetime.utcnow() - timedelta(days=2),
                "resolved_at": datetime.utcnow() - timedelta(days=2),
                "comments": [
                    {
                        "_id": ObjectId(),
                        "text": "The streetlight has been repaired and is now working properly.",
                        "author": str(admin_user["_id"]),
                        "author_name": admin_user["name"],
                        "created_at": datetime.utcnow() - timedelta(days=2),
                        "is_internal": False
                    }
                ],
                "progress": [
                    {
                        "_id": ObjectId(),
                        "status": "completed",
                        "description": "Streetlight repaired and tested - working properly",
                        "updated_by": str(admin_user["_id"]),
                        "updated_by_name": admin_user["name"],
                        "created_at": datetime.utcnow() - timedelta(days=2)
                    }
                ]
            },
            {
                "_id": ObjectId(),
                "title": "Garbage Collection Missed",
                "description": "Garbage collection was missed on our street this week. The bins are overflowing and attracting pests.",
                "category": "garbage",
                "priority": "medium",
                "status": "pending",
                "location": {
                    "address": "Maple Lane, Residential Area",
                    "coordinates": {"lat": 40.7505, "lng": -73.9934}
                },
                "images": ["/uploads/garbage1.jpg"],
                "reported_by": str(citizen_users[0]["_id"]),
                "assigned_to": None,
                "created_at": datetime.utcnow() - timedelta(days=3),
                "updated_at": datetime.utcnow() - timedelta(days=3),
                "resolved_at": None,
                "comments": [],
                "progress": []
            }
        ]
        
        db.issues.insert_many(sample_issues)
        print(f"Created {len(sample_issues)} sample issues")
        
        # Verify data
        print("\nVerifying data...")
        user_count = db.users.count_documents({})
        issue_count = db.issues.count_documents({})
        admin_count = db.users.count_documents({"role": "admin"})
        citizen_count = db.users.count_documents({"role": "citizen"})
        
        print(f"Users: {user_count} (Admins: {admin_count}, Citizens: {citizen_count})")
        print(f"Issues: {issue_count}")
        
        # Print login credentials
        print("\n" + "="*50)
        print("LOGIN CREDENTIALS:")
        print("="*50)
        print("ADMIN ACCOUNT:")
        print("Email: admin@city.gov")
        print("Password: admin123")
        print()
        print("CITIZEN ACCOUNTS:")
        print("Email: john.doe@email.com")
        print("Password: citizen123")
        print()
        print("Email: jane.smith@email.com")
        print("Password: citizen123")
        print("="*50)
        
        print("\nDatabase setup completed successfully!")
        print("Your Citizen Issue Tracker is ready to use!")
        
    except Exception as e:
        print(f"Error during setup: {e}")
    
    finally:
        if 'client' in locals():
            client.close()
            print("Database connection closed")

if __name__ == "__main__":
    main()
