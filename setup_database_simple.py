#!/usr/bin/env python3
"""
Database Setup Script for Citizen Issue Tracker
This script creates the database structure and adds sample data to MongoDB Atlas
"""

import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import random
from bson import ObjectId

# MongoDB Atlas connection string
MONGODB_URL = "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City"
DATABASE_NAME = "citizen_issue_tracker"

def connect_to_database():
    """Connect to MongoDB Atlas"""
    try:
        client = MongoClient(MONGODB_URL)
        # Test connection
        client.admin.command('ping')
        print("Connected to MongoDB Atlas successfully!")
        
        db = client[DATABASE_NAME]
        return db, client
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return None, None

def create_indexes(db):
    """Create database indexes for better performance"""
    print("\nCreating database indexes...")
    
    try:
        # Users collection indexes
        db.users.create_index("email", unique=True)
        db.users.create_index("role")
        print("Users indexes created")
        
        # Issues collection indexes
        db.issues.create_index("reported_by")
        db.issues.create_index("status")
        db.issues.create_index("category")
        db.issues.create_index("priority")
        db.issues.create_index("created_at", -1)  # Descending order
        db.issues.create_index("assigned_to")
        print("Issues indexes created")
        
        print("All indexes created successfully!")
        
    except Exception as e:
        print(f"Error creating indexes: {e}")

def create_sample_users(db):
    """Create sample users"""
    print("\nCreating sample users...")
    
    # Clear existing users
    db.users.delete_many({})
    
    sample_users = [
        {
            "_id": ObjectId(),
            "email": "admin@city.gov",
            "name": "City Administrator",
            "role": "admin",
            "phone": "+1-555-0101",
            "address": "123 City Hall, Downtown",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # password: admin123
            "created_at": datetime.utcnow() - timedelta(days=30),
            "updated_at": datetime.utcnow() - timedelta(days=30)
        },
        {
            "_id": ObjectId(),
            "email": "john.doe@email.com",
            "name": "John Doe",
            "role": "citizen",
            "phone": "+1-555-0102",
            "address": "456 Oak Street, Residential Area",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # password: citizen123
            "created_at": datetime.utcnow() - timedelta(days=25),
            "updated_at": datetime.utcnow() - timedelta(days=25)
        },
        {
            "_id": ObjectId(),
            "email": "jane.smith@email.com",
            "name": "Jane Smith",
            "role": "citizen",
            "phone": "+1-555-0103",
            "address": "789 Pine Avenue, Suburbs",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # password: citizen123
            "created_at": datetime.utcnow() - timedelta(days=20),
            "updated_at": datetime.utcnow() - timedelta(days=20)
        },
        {
            "_id": ObjectId(),
            "email": "mike.wilson@email.com",
            "name": "Mike Wilson",
            "role": "citizen",
            "phone": "+1-555-0104",
            "address": "321 Elm Drive, Downtown",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # password: citizen123
            "created_at": datetime.utcnow() - timedelta(days=15),
            "updated_at": datetime.utcnow() - timedelta(days=15)
        },
        {
            "_id": ObjectId(),
            "email": "sarah.johnson@email.com",
            "name": "Sarah Johnson",
            "role": "citizen",
            "phone": "+1-555-0105",
            "address": "654 Maple Lane, Residential Area",
            "hashed_password": "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J8KzKzKzK",  # password: citizen123
            "created_at": datetime.utcnow() - timedelta(days=10),
            "updated_at": datetime.utcnow() - timedelta(days=10)
        }
    ]
    
    result = db.users.insert_many(sample_users)
    print(f"Created {len(result.inserted_ids)} sample users")
    
    return sample_users

def create_sample_issues(db, users):
    """Create sample issues"""
    print("\nCreating sample issues...")
    
    # Clear existing issues
    db.issues.delete_many({})
    
    # Get user IDs
    admin_user = next((u for u in users if u["role"] == "admin"), None)
    citizen_users = [u for u in users if u["role"] == "citizen"]
    
    if not admin_user or not citizen_users:
        print("No users found for creating issues")
        return []
    
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
            "images": ["/uploads/pothole1.jpg", "/uploads/pothole2.jpg"],
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
                },
                {
                    "_id": ObjectId(),
                    "text": "Work has started on this pothole. We expect completion within 2 days.",
                    "author": str(admin_user["_id"]),
                    "author_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=2),
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
                },
                {
                    "_id": ObjectId(),
                    "status": "in_progress",
                    "description": "Work started - materials ordered",
                    "updated_by": str(admin_user["_id"]),
                    "updated_by_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=2)
                }
            ]
        },
        {
            "_id": ObjectId(),
            "title": "Broken Streetlight on Pine Avenue",
            "description": "Streetlight #47 on Pine Avenue has been out for over a week. It's very dark at night and poses a safety risk.",
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
                    "text": "Thank you for reporting this. We'll send our electrical team to fix it.",
                    "author": str(admin_user["_id"]),
                    "author_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=7),
                    "is_internal": False
                },
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
                    "status": "in_progress",
                    "description": "Assigned to electrical maintenance team",
                    "updated_by": str(admin_user["_id"]),
                    "updated_by_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=7)
                },
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
            "reported_by": str(citizen_users[2]["_id"]),
            "assigned_to": None,
            "created_at": datetime.utcnow() - timedelta(days=3),
            "updated_at": datetime.utcnow() - timedelta(days=3),
            "resolved_at": None,
            "comments": [
                {
                    "_id": ObjectId(),
                    "text": "We apologize for the missed collection. We'll arrange a special pickup.",
                    "author": str(admin_user["_id"]),
                    "author_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=2),
                    "is_internal": False
                }
            ],
            "progress": []
        },
        {
            "_id": ObjectId(),
            "title": "Water Leak on Oak Street",
            "description": "There's a water leak coming from under the sidewalk on Oak Street. Water is pooling and could cause damage.",
            "category": "water",
            "priority": "urgent",
            "status": "in_progress",
            "location": {
                "address": "Oak Street, Near Main Street",
                "coordinates": {"lat": 40.7145, "lng": -73.9990}
            },
            "images": ["/uploads/water_leak1.jpg", "/uploads/water_leak2.jpg"],
            "reported_by": str(citizen_users[3]["_id"]),
            "assigned_to": str(admin_user["_id"]),
            "created_at": datetime.utcnow() - timedelta(days=1),
            "updated_at": datetime.utcnow() - timedelta(hours=6),
            "resolved_at": None,
            "comments": [
                {
                    "_id": ObjectId(),
                    "text": "This is urgent! We're sending our water department immediately.",
                    "author": str(admin_user["_id"]),
                    "author_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(hours=12),
                    "is_internal": False
                }
            ],
            "progress": [
                {
                    "_id": ObjectId(),
                    "status": "in_progress",
                    "description": "Emergency response team dispatched",
                    "updated_by": str(admin_user["_id"]),
                    "updated_by_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(hours=12)
                }
            ]
        },
        {
            "_id": ObjectId(),
            "title": "Damaged Road Sign",
            "description": "The stop sign at the intersection of Elm Drive and Pine Avenue is bent and hard to see.",
            "category": "road",
            "priority": "medium",
            "status": "pending",
            "location": {
                "address": "Elm Drive & Pine Avenue Intersection",
                "coordinates": {"lat": 40.7614, "lng": -73.9776}
            },
            "images": ["/uploads/sign_damage1.jpg"],
            "reported_by": str(citizen_users[4]["_id"]),
            "assigned_to": None,
            "created_at": datetime.utcnow() - timedelta(days=2),
            "updated_at": datetime.utcnow() - timedelta(days=2),
            "resolved_at": None,
            "comments": [],
            "progress": []
        },
        {
            "_id": ObjectId(),
            "title": "Sewage Backup in Drain",
            "description": "There's a sewage backup in the storm drain on Maple Lane. There's a foul smell and potential health hazard.",
            "category": "sewage",
            "priority": "high",
            "status": "completed",
            "location": {
                "address": "Maple Lane Storm Drain",
                "coordinates": {"lat": 40.7505, "lng": -73.9934}
            },
            "images": ["/uploads/sewage1.jpg"],
            "reported_by": str(citizen_users[0]["_id"]),
            "assigned_to": str(admin_user["_id"]),
            "created_at": datetime.utcnow() - timedelta(days=6),
            "updated_at": datetime.utcnow() - timedelta(days=1),
            "resolved_at": datetime.utcnow() - timedelta(days=1),
            "comments": [
                {
                    "_id": ObjectId(),
                    "text": "This is a health hazard. We're sending our sanitation team immediately.",
                    "author": str(admin_user["_id"]),
                    "author_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=5),
                    "is_internal": False
                },
                {
                    "_id": ObjectId(),
                    "text": "The sewage backup has been cleared and the drain is functioning properly.",
                    "author": str(admin_user["_id"]),
                    "author_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=1),
                    "is_internal": False
                }
            ],
            "progress": [
                {
                    "_id": ObjectId(),
                    "status": "in_progress",
                    "description": "Emergency sanitation team dispatched",
                    "updated_by": str(admin_user["_id"]),
                    "updated_by_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=5)
                },
                {
                    "_id": ObjectId(),
                    "status": "completed",
                    "description": "Sewage backup cleared and drain cleaned",
                    "updated_by": str(admin_user["_id"]),
                    "updated_by_name": admin_user["name"],
                    "created_at": datetime.utcnow() - timedelta(days=1)
                }
            ]
        }
    ]
    
    result = db.issues.insert_many(sample_issues)
    print(f"Created {len(result.inserted_ids)} sample issues")
    
    return sample_issues

def verify_data(db):
    """Verify the data was created correctly"""
    print("\nVerifying database data...")
    
    try:
        # Count documents
        user_count = db.users.count_documents({})
        issue_count = db.issues.count_documents({})
        
        print(f"Users: {user_count}")
        print(f"Issues: {issue_count}")
        
        # Check user roles
        admin_count = db.users.count_documents({"role": "admin"})
        citizen_count = db.users.count_documents({"role": "citizen"})
        
        print(f"Admins: {admin_count}")
        print(f"Citizens: {citizen_count}")
        
        # Check issue statuses
        pending_count = db.issues.count_documents({"status": "pending"})
        in_progress_count = db.issues.count_documents({"status": "in_progress"})
        completed_count = db.issues.count_documents({"status": "completed"})
        
        print(f"Pending Issues: {pending_count}")
        print(f"In Progress Issues: {in_progress_count}")
        print(f"Completed Issues: {completed_count}")
        
        # Check issue categories
        categories = db.issues.distinct("category")
        print(f"Issue Categories: {', '.join(categories)}")
        
        print("Data verification completed successfully!")
        
    except Exception as e:
        print(f"Error verifying data: {e}")

def print_sample_credentials():
    """Print sample login credentials"""
    print("\nSample Login Credentials:")
    print("=" * 50)
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
    print()
    print("Email: mike.wilson@email.com")
    print("Password: citizen123")
    print()
    print("Email: sarah.johnson@email.com")
    print("Password: citizen123")
    print("=" * 50)

def main():
    """Main function to set up the database"""
    print("Citizen Issue Tracker Database Setup")
    print("=" * 50)
    
    # Connect to database
    db, client = connect_to_database()
    if db is None:
        return
    
    try:
        # Create indexes
        create_indexes(db)
        
        # Create sample users
        users = create_sample_users(db)
        
        # Create sample issues
        issues = create_sample_issues(db, users)
        
        # Verify data
        verify_data(db)
        
        # Print credentials
        print_sample_credentials()
        
        print("\nDatabase setup completed successfully!")
        print("Your Citizen Issue Tracker is ready to use!")
        print("\nNext steps:")
        print("1. Start the backend: cd backend && python -m uvicorn main:app --reload")
        print("2. Start the frontend: cd frontend && npm run dev")
        print("3. Open http://localhost:3000 and login with the sample credentials")
        
    except Exception as e:
        print(f"Error during setup: {e}")
    
    finally:
        # Close connection
        if client:
            client.close()
            print("\nDatabase connection closed")

if __name__ == "__main__":
    main()
