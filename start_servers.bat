@echo off
echo Starting Citizen Issue Tracker...

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs

pause
