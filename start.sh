#!/bin/bash

echo "Starting Citizen Issue Tracker..."
echo

# Check if MongoDB is running
if ! pgrep -x "mongod" > /dev/null; then
    echo "MongoDB is not running. Starting MongoDB..."
    
    # Try different ways to start MongoDB based on OS
    if command -v brew &> /dev/null; then
        # macOS with Homebrew
        brew services start mongodb/brew/mongodb-community
    elif command -v systemctl &> /dev/null; then
        # Linux with systemd
        sudo systemctl start mongod
    else
        echo "Please start MongoDB manually and run this script again."
        exit 1
    fi
    
    # Wait a moment for MongoDB to start
    sleep 3
fi

echo "MongoDB is running."
echo

echo "Starting the application..."
npm run dev
