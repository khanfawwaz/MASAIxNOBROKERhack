#!/usr/bin/env python3
"""
Email Service Test Script
This script tests the SendGrid email functionality
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from email_service import email_service

async def test_email_service():
    print("Testing SendGrid Email Service...")
    print("=" * 40)
    
    # Test email (replace with your email for testing)
    test_email = "test@example.com"  # Replace with your actual email
    
    print(f"Testing with email: {test_email}")
    print("Note: Replace 'test@example.com' with your actual email address for testing")
    
    try:
        # Test 1: Welcome Email
        print("\n1. Testing Welcome Email...")
        success = await email_service.send_welcome_email(
            test_email,
            "Test User",
            "citizen"
        )
        if success:
            print("   Welcome email sent successfully!")
        else:
            print("   Welcome email failed!")
        
        # Test 2: Login Notification
        print("\n2. Testing Login Notification...")
        success = await email_service.send_login_notification(
            test_email,
            "Test User",
            "2025-10-25 08:30:00 UTC"
        )
        if success:
            print("   Login notification sent successfully!")
        else:
            print("   Login notification failed!")
        
        # Test 3: Issue Update Email
        print("\n3. Testing Issue Update Email...")
        success = await email_service.send_issue_update_email(
            test_email,
            "Test User",
            "Test Pothole Issue",
            "in_progress",
            "Work has started on fixing this pothole. Expected completion in 2 days.",
            "507f1f77bcf86cd799439011"
        )
        if success:
            print("   Issue update email sent successfully!")
        else:
            print("   Issue update email failed!")
        
        print("\n" + "=" * 40)
        print("Email service test completed!")
        print("\nTo test with real emails:")
        print("1. Replace 'test@example.com' with your actual email")
        print("2. Run this script again")
        print("3. Check your email inbox for the test emails")
        
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    asyncio.run(test_email_service())
