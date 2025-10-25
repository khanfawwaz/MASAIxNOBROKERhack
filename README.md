# Citizen Issue Tracker

A comprehensive web application for citizens to report and track local issues like potholes, garbage, streetlight failures, and more. The system includes separate dashboards for citizens and administrators/authorities.

## Features

### For Citizens
- **Issue Reporting**: Report various types of issues with photos and location
- **Issue Tracking**: Track the status of reported issues (Pending, In Progress, Completed)
- **Real-time Updates**: Receive updates on issue progress
- **User Profile**: Manage personal information and view statistics

### For Administrators/Authorities
- **Issue Management**: View and manage all reported issues
- **Status Updates**: Update issue status and add progress notes
- **Analytics Dashboard**: View statistics and charts for better insights
- **User Management**: Manage user accounts and permissions
- **Assignment**: Assign issues to specific team members

## Technology Stack

### Frontend
- **React 18** with TypeScript
- **Vite** for fast development and building
- **Tailwind CSS** for styling
- **React Router** for navigation
- **React Query** for data fetching
- **React Hook Form** for form handling
- **Lucide React** for icons
- **Recharts** for data visualization

### Backend
- **FastAPI** (Python 3.8+)
- **MongoDB** with Motor (async driver)
- **Pydantic** for data validation
- **JWT** for authentication
- **Bcrypt** for password hashing
- **Python-multipart** for file uploads

## Project Structure

```
citizen-issue-tracker/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── contexts/       # React contexts
│   │   ├── services/       # API services
│   │   ├── types/          # TypeScript types
│   │   └── main.tsx        # Entry point
│   ├── package.json
│   └── vite.config.ts
├── backend/                 # FastAPI backend
│   ├── routers/            # API routes
│   ├── models.py           # Pydantic models
│   ├── auth.py             # Authentication utilities
│   ├── database.py         # Database connection
│   ├── main.py             # FastAPI app
│   └── requirements.txt
└── README.md
```

## Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- MongoDB 4.4+

### 1. Clone the Repository
```bash
git clone <repository-url>
cd citizen-issue-tracker
```

### 2. Install Dependencies
```bash
# Install all dependencies
npm run install:all

# Or install separately:
# Frontend
cd frontend && npm install

# Backend
cd backend && pip install -r requirements.txt
```

### 3. MongoDB Setup
See [MongoDB Setup Guide](#mongodb-setup-guide) below.

### 4. Environment Configuration
```bash
# Copy environment file
cp backend/env.example backend/.env

# Edit the .env file with your configuration
```

### 5. Run the Application
```bash
# Start both frontend and backend
npm run dev

# Or start separately:
# Frontend (port 3000)
npm run dev:frontend

# Backend (port 8000)
npm run dev:backend
```

## MongoDB Setup Guide

### Option 1: Local MongoDB Installation

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the setup wizard
3. Start MongoDB service:
   ```cmd
   net start MongoDB
   ```

#### macOS
```bash
# Install using Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

#### Linux (Ubuntu/Debian)
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create list file
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update package database
sudo apt-get update

# Install MongoDB
sudo apt-get install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod
```

### Option 2: MongoDB Atlas (Cloud)
1. Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a free account
3. Create a new cluster
4. Get your connection string
5. Update `MONGODB_URL` in your `.env` file

### Option 3: Docker
```bash
# Run MongoDB in Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or with persistent storage
docker run -d -p 27017:27017 --name mongodb -v mongodb_data:/data/db mongo:latest
```

### Database Configuration
1. MongoDB will be accessible at `mongodb://localhost:27017`
2. The application will automatically create the database `citizen_issue_tracker`
3. Collections will be created automatically when data is inserted

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user info
- `PUT /auth/profile` - Update user profile

#### Issues
- `GET /issues` - Get user's issues (citizens) or all issues (admins)
- `POST /issues` - Create new issue
- `GET /issues/{id}` - Get issue details
- `PUT /issues/{id}` - Update issue
- `POST /issues/{id}/comments` - Add comment
- `POST /issues/{id}/progress` - Add progress update

#### Admin
- `GET /admin/issues` - Get all issues with filters
- `GET /admin/stats` - Get dashboard statistics
- `PUT /admin/issues/{id}/assign` - Assign issue to user

## Usage

### For Citizens
1. Register/Login to the application
2. Click "Report New Issue" to create a new issue
3. Fill in the issue details, upload photos, and set location
4. Track your issues in the dashboard
5. View detailed information and add comments

### For Administrators
1. Login with admin credentials
2. View the admin dashboard with statistics
3. Manage all reported issues
4. Update issue status and add progress notes
5. Assign issues to team members

## Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd backend
uvicorn main:app --reload    # Start development server
python -m pytest            # Run tests (if implemented)
```

### Code Structure
- **Frontend**: Component-based architecture with TypeScript
- **Backend**: FastAPI with async/await patterns
- **Database**: MongoDB with Motor async driver
- **Authentication**: JWT tokens with role-based access

## Deployment

### Frontend (Vercel/Netlify)
1. Build the frontend: `npm run build`
2. Deploy the `dist` folder to your hosting service
3. Update API URLs in production

### Backend (Railway/Heroku/DigitalOcean)
1. Set environment variables
2. Deploy the backend code
3. Ensure MongoDB is accessible
4. Configure CORS for your frontend domain

### Database
- Use MongoDB Atlas for production
- Set up proper authentication and network access
- Configure backups and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.

---

**Note**: This is a demo application. For production use, ensure proper security measures, error handling, and testing are implemented.