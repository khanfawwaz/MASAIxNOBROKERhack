# Citizen Issue Tracker

A comprehensive web application for citizens to report local issues (potholes, garbage, streetlight failures, etc.) and for authorities to manage and track these issues.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.8+
- MongoDB Atlas account

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd MASAIxNOBROKERhack
   ```

2. **Setup Environment Variables**
   - Copy `env_template.txt` to `backend/.env`
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
   npm run dev
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

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

Create a `backend/.env` file with the following variables:

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

# Server Configuration
BACKEND_PORT=8000
FRONTEND_PORT=3000
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
│   ├── src/
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   ├── contexts/     # React contexts
│   │   ├── hooks/        # Custom React hooks
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript type definitions
│   └── public/           # Static assets
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
- Build Tool: Vite
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

## 🚀 Deployment

### Backend Deployment
1. Set up production environment variables
2. Use a production ASGI server like Gunicorn
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates

### Frontend Deployment
1. Build the production bundle: `npm run build`
2. Serve static files with a web server
3. Configure API endpoint URLs

## 🔒 Security Considerations

- Change default admin credentials
- Use strong JWT secret keys
- Implement rate limiting
- Validate file uploads
- Use HTTPS in production
- Regular security updates
