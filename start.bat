@echo off
echo Starting Citizen Issue Tracker...
echo.

echo Checking if MongoDB is running...
net start MongoDB >nul 2>&1
if %errorlevel% neq 0 (
    echo MongoDB is not running. Starting MongoDB...
    net start MongoDB
    if %errorlevel% neq 0 (
        echo Failed to start MongoDB. Please start it manually.
        pause
        exit /b 1
    )
)

echo MongoDB is running.
echo.

echo Starting the application...
npm run dev

pause
