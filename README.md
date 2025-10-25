# Citizen Issue Tracker

A comprehensive web application for citizens to report local issues (potholes, garbage, streetlight failures, etc.) and for authorities to manage and track these issues.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- MongoDB Atlas account
- Vercel account (for deployment)

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MASAIxNOBROKERhack
   ```

2. **Setup Environment Variables**
   - Copy `env_template.txt` to `backend/.env`
   - Copy `frontend/env.example` to `frontend/.env.local`
   - Update the API keys and configuration as needed

3. **Install Dependencies**

   **Backend:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

   **Frontend:**
   ```bash
   cd frontend
   npm install
   ```

4. **Run the Application**

   **Start Backend Server:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload --port 8000
   ```

   **Start Frontend Server:**
   ```bash
   cd frontend
   npm install  # Install dependencies first
   npm start
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🚀 Vercel Deployment

### Prerequisites for Deployment
- Vercel account
- MongoDB Atlas database
- SendGrid account (for email notifications)

### Step 1: Deploy Backend to Vercel

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy Backend**
   ```bash
   cd backend
   vercel --prod
   ```

3. **Configure Environment Variables in Vercel Dashboard**
   - Go to your project settings in Vercel
   - Add the following environment variables:
     ```
     MONGODB_URL=your_mongodb_connection_string
     DATABASE_NAME=citizen_issue_tracker
     SENDGRID_API_KEY=your_sendgrid_api_key
     FROM_EMAIL=noreply@yourdomain.com
     FROM_NAME=Your App Name
     SECRET_KEY=your-secret-key-here
     ALGORITHM=HS256
     ACCESS_TOKEN_EXPIRE_MINUTES=30
     ```

### Step 2: Deploy Frontend to Vercel

1. **Deploy Frontend**
   ```bash
   cd frontend
   vercel --prod
   ```

2. **Configure Environment Variables**
   - In Vercel dashboard, add:
     ```
     REACT_APP_API_URL=https://your-backend-api.vercel.app
     ```

### Step 3: Configure Custom Domain (Optional)

1. Go to your Vercel project settings
2. Add your custom domain
3. Configure DNS records as instructed by Vercel

## 📋 Features

### For Citizens
- **Report Issues**: Upload photos and details of local problems
- **Track Progress**: Monitor status updates on reported issues
- **View Updates**: Receive notifications and comments from authorities
- **Profile Management**: Update personal information

### For Administrators
- **Issue Management**: View, assign, and update issue status
- **Dashboard Analytics**: Statistics and progress tracking
- **User Management**: Handle citizen accounts and permissions
- **Email Notifications**: Automated updates to citizens

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
# MongoDB Configuration
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=citizen_issue_tracker

# SendGrid Email Configuration
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=noreply@yourdomain.com
FROM_NAME=Your App Name

# JWT Configuration
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env.local):**
```env
# API Configuration
REACT_APP_API_URL=http://localhost:8000
```

### Database Setup

The application automatically connects to MongoDB Atlas. Ensure your connection string is correct in the environment variables.

## 🏗️ Project Structure

```
├── backend/
│   ├── routers/          # API route handlers
│   ├── models.py         # Pydantic data models
│   ├── auth.py           # Authentication utilities
│   ├── database.py       # Database connection
│   ├── email_service.py  # Email notification service
│   └── main.py           # FastAPI application
├── frontend/
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── contexts/     # React contexts
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript type definitions
│   ├── package.json      # Dependencies and scripts
│   └── vercel.json       # Vercel configuration
├── vercel.json           # Root Vercel configuration
└── README.md
```

## 🔐 Authentication

### User Roles
- **Citizen**: Can report issues and view their own reports
- **Admin**: Can manage all issues and user accounts

### Default Admin Account
- Email: `admin@example.com`
- Password: `admin123`

## 📧 Email Notifications

The system sends automated emails for:
- Welcome messages on registration
- Login notifications for security
- Issue status updates
- New comments on issues

## 🛠️ Development

### Backend Development
- Framework: FastAPI
- Database: MongoDB with Motor (async driver)
- Authentication: JWT tokens
- Email: SendGrid integration

### Frontend Development
- Framework: React 18 with TypeScript
- Build Tool: Create React App
- Styling: Tailwind CSS
- State Management: React Query
- Forms: React Hook Form
- Icons: Lucide React

### API Endpoints

**Authentication:**
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user

**Issues:**
- `GET /issues` - List issues
- `POST /issues` - Create new issue
- `GET /issues/{id}` - Get issue details
- `PUT /issues/{id}` - Update issue
- `POST /issues/{id}/comments` - Add comment

**Admin:**
- `GET /admin/issues` - Admin issue management
- `GET /admin/stats` - Dashboard statistics

## 🔒 Security Considerations

- Change default admin credentials
- Use strong JWT secret keys
- Implement rate limiting
- Validate file uploads
- Use HTTPS in production
- Regular security updates

## 🚀 Production Deployment Checklist

### Backend Deployment
- [ ] Set up MongoDB Atlas database
- [ ] Configure SendGrid for email notifications
- [ ] Set up environment variables in Vercel
- [ ] Deploy backend to Vercel
- [ ] Test API endpoints

### Frontend Deployment
- [ ] Update API URL in environment variables
- [ ] Deploy frontend to Vercel
- [ ] Configure custom domain (optional)
- [ ] Test all functionality

### Post-Deployment
- [ ] Update admin credentials
- [ ] Test email notifications
- [ ] Verify file uploads work
- [ ] Test user registration and login
- [ ] Check issue reporting functionality

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Ensure backend CORS settings include your frontend domain
   - Check environment variables are set correctly

2. **API Connection Issues**
   - Verify `REACT_APP_API_URL` is set correctly
   - Check if backend is deployed and accessible

3. **Database Connection Issues**
   - Verify MongoDB connection string
   - Check if database name is correct

4. **Email Notifications Not Working**
   - Verify SendGrid API key
   - Check email templates and configuration

### Support

For issues and questions:
- Check the API documentation at `/docs` endpoint
- Review environment variable configuration
- Ensure all dependencies are installed correctly
