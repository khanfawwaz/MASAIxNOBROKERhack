#!/usr/bin/env python3
"""
Admin Login Test Script
This script tests the complete admin login flow
"""

import requests
import json

def test_admin_login():
    print("Testing Admin Login Flow...")
    print("=" * 40)
    
    base_url = "http://localhost:8000"
    
    try:
        # Step 1: Test login
        print("1. Testing admin login...")
        login_data = {
            "email": "admin@city.gov",
            "password": "admin123"
        }
        
        response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            print("   Login successful!")
            data = response.json()
            token = data["access_token"]
            user = data["user"]
            print(f"   User: {user['name']} ({user['role']})")
            print(f"   Token: {token[:50]}...")
        else:
            print(f"   Login failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Step 2: Test /auth/me
        print("\n2. Testing /auth/me endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{base_url}/auth/me", headers=headers)
        
        if response.status_code == 200:
            print("   /auth/me successful!")
            user_data = response.json()
            print(f"   User data: {user_data['name']} ({user_data['role']})")
        else:
            print(f"   /auth/me failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Step 3: Test admin stats
        print("\n3. Testing admin stats endpoint...")
        response = requests.get(f"{base_url}/admin/stats", headers=headers)
        
        if response.status_code == 200:
            print("   Admin stats successful!")
            stats = response.json()
            print(f"   Stats: {stats}")
        else:
            print(f"   Admin stats failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        # Step 4: Test admin issues
        print("\n4. Testing admin issues endpoint...")
        response = requests.get(f"{base_url}/admin/issues", headers=headers)
        
        if response.status_code == 200:
            print("   Admin issues successful!")
            issues = response.json()
            print(f"   Found {len(issues)} issues")
        else:
            print(f"   Admin issues failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
        
        print("\nAll tests passed! Admin login is working correctly.")
        return True
        
    except Exception as e:
        print(f"Error during testing: {e}")
        return False

if __name__ == "__main__":
    test_admin_login()
