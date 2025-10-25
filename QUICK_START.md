# Quick Start Guide - Citizen Issue Tracker

Get up and running with the Citizen Issue Tracker in under 10 minutes!

## Prerequisites Checklist

- [ ] Node.js 18+ installed
- [ ] Python 3.8+ installed
- [ ] MongoDB installed and running
- [ ] Git installed

## Step 1: Clone and Install

```bash
# Clone the repository
git clone <your-repo-url>
cd citizen-issue-tracker

# Install all dependencies
npm run install:all
```

## Step 2: Set Up MongoDB

### Option A: Local MongoDB (Quickest)
```bash
# Windows
net start MongoDB

# macOS
brew services start mongodb/brew/mongodb-community

# Linux
sudo systemctl start mongod
```

### Option B: Docker (Alternative)
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Option C: MongoDB Atlas (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create free account and cluster
3. Get connection string
4. Update `.env` file (see Step 3)

## Step 3: Configure Environment

```bash
# Copy environment file
cp backend/env.example backend/.env

# Edit the .env file
# For local MongoDB, keep default values:
# MONGODB_URL=mongodb://localhost:27017
# DATABASE_NAME=citizen_issue_tracker
# SECRET_KEY=your-super-secret-key-here
```

## Step 4: Start the Application

```bash
# Start both frontend and backend
npm run dev
```

This will start:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Step 5: Create Your First Account

1. Open http://localhost:3000
2. Click "Sign up"
3. Create an admin account:
   - Name: Admin User
   - Email: admin@example.com
   - Password: admin123
   - Role: Admin/Authority
4. Click "Create Account"

## Step 6: Test the Application

### As a Citizen:
1. Create a citizen account
2. Report a new issue with photos
3. Track the issue status

### As an Admin:
1. Login with admin account
2. View the admin dashboard
3. Manage reported issues
4. Update issue status

## Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
# Windows
net start MongoDB

# macOS/Linux
brew services list | grep mongo
# or
sudo systemctl status mongod
```

### Port Already in Use
```bash
# Kill processes on ports 3000 and 8000
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

### Python Dependencies Issues
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Node.js Dependencies Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## What's Next?

1. **Customize the Application**
   - Update branding and colors in `frontend/tailwind.config.js`
   - Modify issue categories in `backend/models.py`
   - Add new features

2. **Deploy to Production**
   - Set up MongoDB Atlas for production
   - Deploy backend to Railway/Heroku
   - Deploy frontend to Vercel/Netlify

3. **Add More Features**
   - Email notifications
   - Push notifications
   - Mobile app
   - Advanced analytics

## Need Help?

- Check the [Full README](README.md) for detailed documentation
- See [MongoDB Setup Guide](MONGODB_SETUP.md) for database configuration
- Open an issue in the repository for support

## Default Credentials

After setup, you can use these test accounts:

**Admin Account:**
- Email: admin@example.com
- Password: admin123

**Citizen Account:**
- Email: citizen@example.com
- Password: citizen123

*Note: Change these passwords in production!*

---

**Happy coding! 🚀**
