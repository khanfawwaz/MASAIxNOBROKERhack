# Troubleshooting Guide - Citizen Issue Tracker

## Common Issues and Solutions

### 1. React Router Warnings
**Issue**: Future flag warnings about React Router v7
**Solution**: ✅ **FIXED** - Added future flags to BrowserRouter in `main.tsx`

### 2. API 404 Errors
**Issue**: `Failed to load resource: the server responded with a status of 404 (Not Found)`
**Solution**: 
- ✅ **Backend server is running** on port 8000
- ✅ **Frontend server is running** on port 3000
- ✅ **Vite proxy configured** to rewrite `/api` requests

### 3. Server Startup Issues

#### Backend Server
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

#### Frontend Server
```bash
cd frontend
npm run dev
```

### 4. Database Connection Issues
**Issue**: MongoDB connection errors
**Solution**: 
- ✅ **MongoDB Atlas connected** successfully
- ✅ **Sample data created** (3 users, 3 issues)
- ✅ **Database indexes** created

### 5. Authentication Issues
**Issue**: Login/registration not working
**Solution**: Use the provided test credentials:

```
ADMIN ACCOUNT:
Email: admin@city.gov
Password: admin123

CITIZEN ACCOUNTS:
Email: john.doe@email.com
Password: citizen123

Email: jane.smith@email.com
Password: citizen123
```

### 6. Port Conflicts
**Issue**: Ports 3000 or 8000 already in use
**Solution**:
```bash
# Kill processes on ports
netstat -ano | findstr :3000
taskkill /PID <PID> /F

netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 7. API Proxy Issues
**Issue**: Frontend can't reach backend API
**Solution**: 
- Check Vite proxy configuration in `vite.config.ts`
- Ensure both servers are running
- Test API directly: `http://localhost:8000/health`

### 8. CORS Issues
**Issue**: Cross-origin requests blocked
**Solution**: ✅ **FIXED** - CORS middleware configured in backend

### 9. File Upload Issues
**Issue**: Image uploads not working
**Solution**: 
- Check `uploads` directory exists
- Verify file size limits
- Check file type restrictions

### 10. Environment Variables
**Issue**: Missing environment configuration
**Solution**: 
- MongoDB connection string is hardcoded in the application
- No `.env` file needed for basic setup

## Quick Start Commands

### Option 1: Manual Start
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### Option 2: Batch Script
```bash
# Windows
start_servers.bat
```

### Option 3: Using npm scripts
```bash
# From project root
npm run dev
```

## Verification Steps

1. **Backend Health Check**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Frontend Access**:
   - Open http://localhost:3000
   - Should see login page

3. **API Documentation**:
   - Open http://localhost:8000/docs
   - Should see FastAPI docs

4. **Database Verification**:
   ```bash
   python verify_db.py
   ```

## Current Status

✅ **Backend Server**: Running on port 8000
✅ **Frontend Server**: Running on port 3000  
✅ **Database**: Connected to MongoDB Atlas
✅ **Sample Data**: 3 users, 3 issues created
✅ **API Endpoints**: All working
✅ **Authentication**: JWT tokens working
✅ **CORS**: Configured properly
✅ **React Router**: Future flags added

## Next Steps

1. **Access the application**: http://localhost:3000
2. **Login with test credentials**
3. **Test issue reporting** as a citizen
4. **Test issue management** as an admin
5. **Verify all features** are working

## Support

If you encounter any issues:
1. Check this troubleshooting guide
2. Verify both servers are running
3. Check browser console for errors
4. Test API endpoints directly
5. Restart both servers if needed
