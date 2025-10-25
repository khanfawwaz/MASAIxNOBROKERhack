#!/usr/bin/env python3
"""
Fix Admin Password Script
This script will properly hash the admin password and update the database
"""

import pymongo
from pymongo import MongoClient
from passlib.context import CryptContext
from bson import ObjectId

# MongoDB Atlas connection string
MONGODB_URL = "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City"
DATABASE_NAME = "citizen_issue_tracker"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_admin_password():
    print("Fixing Admin Password...")
    print("=" * 30)
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URL)
        client.admin.command('ping')
        print("Connected to MongoDB Atlas successfully!")
        
        db = client[DATABASE_NAME]
        
        # Find admin user
        admin_user = db.users.find_one({"email": "admin@city.gov"})
        
        if not admin_user:
            print("ERROR: Admin user not found!")
            return False
        
        print(f"Found admin user: {admin_user['name']}")
        
        # Hash the password properly
        plain_password = "admin123"
        hashed_password = pwd_context.hash(plain_password)
        
        print("Password hashed successfully!")
        
        # Update the admin user with proper password hash
        result = db.users.update_one(
            {"_id": admin_user["_id"]},
            {"$set": {"hashed_password": hashed_password}}
        )
        
        if result.modified_count > 0:
            print("Admin password updated successfully!")
            
            # Verify the update
            updated_user = db.users.find_one({"_id": admin_user["_id"]})
            print(f"Updated user: {updated_user['email']}")
            
            # Test password verification
            if pwd_context.verify(plain_password, updated_user["hashed_password"]):
                print("Password verification successful!")
                return True
            else:
                print("ERROR: Password verification failed!")
                return False
        else:
            print("ERROR: Failed to update admin password!")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    finally:
        if 'client' in locals():
            client.close()
            print("Database connection closed")

if __name__ == "__main__":
    if fix_admin_password():
        print("\nSUCCESS: Admin password fixed!")
        print("You can now login with:")
        print("Email: admin@city.gov")
        print("Password: admin123")
    else:
        print("\nFAILED: Could not fix admin password")
