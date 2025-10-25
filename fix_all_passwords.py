#!/usr/bin/env python3
"""
Fix All User Passwords Script
This script will properly hash all user passwords
"""

import pymongo
from pymongo import MongoClient
from passlib.context import CryptContext

# MongoDB Atlas connection string
MONGODB_URL = "mongodb+srv://Oratio:Ol3p6g2M1Q70hDzL@my-city.yasqkwz.mongodb.net/?appName=My-City"
DATABASE_NAME = "citizen_issue_tracker"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def fix_all_passwords():
    print("Fixing All User Passwords...")
    print("=" * 35)
    
    try:
        # Connect to MongoDB
        client = MongoClient(MONGODB_URL)
        client.admin.command('ping')
        print("Connected to MongoDB Atlas successfully!")
        
        db = client[DATABASE_NAME]
        
        # Define user credentials
        user_credentials = [
            {"email": "admin@city.gov", "password": "admin123", "role": "admin"},
            {"email": "john.doe@email.com", "password": "citizen123", "role": "citizen"},
            {"email": "jane.smith@email.com", "password": "citizen123", "role": "citizen"}
        ]
        
        updated_count = 0
        
        for cred in user_credentials:
            # Find user
            user = db.users.find_one({"email": cred["email"]})
            
            if user:
                print(f"Updating {cred['role']}: {cred['email']}")
                
                # Hash the password
                hashed_password = pwd_context.hash(cred["password"])
                
                # Update the user
                result = db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"hashed_password": hashed_password}}
                )
                
                if result.modified_count > 0:
                    print(f"  Password updated successfully!")
                    updated_count += 1
                else:
                    print(f"  Password was already correct")
                    updated_count += 1
            else:
                print(f"User not found: {cred['email']}")
        
        print(f"\nUpdated {updated_count} users successfully!")
        
        # Test all logins
        print("\nTesting all logins...")
        for cred in user_credentials:
            user = db.users.find_one({"email": cred["email"]})
            if user and pwd_context.verify(cred["password"], user["hashed_password"]):
                print(f"  {cred['email']}: Login test PASSED")
            else:
                print(f"  {cred['email']}: Login test FAILED")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False
    
    finally:
        if 'client' in locals():
            client.close()
            print("Database connection closed")

if __name__ == "__main__":
    if fix_all_passwords():
        print("\nSUCCESS: All passwords fixed!")
        print("\nLogin Credentials:")
        print("ADMIN:")
        print("  Email: admin@city.gov")
        print("  Password: admin123")
        print("\nCITIZENS:")
        print("  Email: john.doe@email.com")
        print("  Password: citizen123")
        print("  Email: jane.smith@email.com")
        print("  Password: citizen123")
    else:
        print("\nFAILED: Could not fix passwords")
