# Login Guide - Citizen Issue Tracker

## 🔐 Admin Login Fixed!

The admin login issue has been resolved! All user passwords have been properly hashed and are now working correctly.

## ✅ **Working Login Credentials**

### **ADMIN ACCOUNT**
```
Email: admin@city.gov
Password: admin123
```
**Access**: Full admin dashboard with issue management capabilities

### **CITIZEN ACCOUNTS**
```
Email: john.doe@email.com
Password: citizen123

Email: jane.smith@email.com
Password: citizen123
```
**Access**: Citizen dashboard for reporting and tracking issues

## 🚀 **How to Login**

1. **Open the application**: http://localhost:3001
2. **Click "Login"** or go to the login page
3. **Enter credentials** from the list above
4. **Click "Sign In"**
5. **You'll be redirected** to the appropriate dashboard:
   - **Admin** → Admin Dashboard
   - **Citizen** → Citizen Dashboard

## 🔧 **What Was Fixed**

### **Problem**
- Admin login was failing with "Incorrect email or password"
- Passwords in database weren't properly hashed
- Authentication system couldn't verify credentials

### **Solution**
1. **Fixed password hashing** using bcrypt
2. **Updated all user passwords** in the database
3. **Verified authentication** for all accounts
4. **Tested login functionality** for both admin and citizens

## 📊 **Admin Dashboard Features**

Once logged in as admin, you can:

- **View all reported issues** from citizens
- **Update issue status** (pending → in progress → completed)
- **Assign issues** to team members
- **Add comments** and progress updates
- **Manage issue priorities**
- **View analytics** and reports
- **Access admin-only features**

## 👥 **Citizen Dashboard Features**

Once logged in as a citizen, you can:

- **Report new issues** with photos and location
- **Track your reported issues**
- **View issue status** and updates
- **Add comments** to your issues
- **Update your profile**
- **View issue history**

## 🛠️ **Troubleshooting**

### **If Login Still Fails**
1. **Check server status**: Make sure backend is running on port 8000
2. **Clear browser cache**: Try refreshing the page
3. **Check credentials**: Use exact email and password from the list
4. **Check network**: Ensure frontend can reach backend API

### **Server Status Check**
```bash
# Backend should be running on:
http://localhost:8000

# Frontend should be running on:
http://localhost:3001 (or 3000)
```

### **API Test**
```bash
# Test admin login via API:
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@city.gov","password":"admin123"}'
```

## 🎯 **Next Steps**

1. **Login as admin** to test admin features
2. **Login as citizen** to test citizen features
3. **Report a test issue** as a citizen
4. **Manage the issue** as an admin
5. **Test the complete workflow**

## 📝 **Additional Notes**

- **JWT tokens** are used for authentication
- **Sessions last** 30 minutes by default
- **Passwords are securely hashed** with bcrypt
- **CORS is configured** for both ports 3000 and 3001
- **All API endpoints** are working correctly

The login system is now fully functional! 🎉
