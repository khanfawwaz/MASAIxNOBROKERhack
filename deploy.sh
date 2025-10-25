#!/bin/bash

# Citizen Issue Tracker - Deployment Script
# This script helps deploy the application to Vercel

echo "🚀 Citizen Issue Tracker Deployment Script"
echo "=========================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed. Installing now..."
    npm install -g vercel
fi

echo ""
echo "📋 Deployment Checklist:"
echo "1. ✅ Vercel CLI installed"
echo "2. ⏳ Deploying backend..."
echo "3. ⏳ Deploying frontend..."
echo "4. ⏳ Configuring environment variables..."

# Deploy Backend
echo ""
echo "🔧 Deploying Backend to Vercel..."
cd backend
vercel --prod --yes
BACKEND_URL=$(vercel ls | grep backend | awk '{print $2}' | head -1)
echo "✅ Backend deployed to: $BACKEND_URL"

# Deploy Frontend
echo ""
echo "🔧 Deploying Frontend to Vercel..."
cd ../frontend
vercel --prod --yes
FRONTEND_URL=$(vercel ls | grep frontend | awk '{print $2}' | head -1)
echo "✅ Frontend deployed to: $FRONTEND_URL"

echo ""
echo "🎉 Deployment Complete!"
echo "======================"
echo "Backend URL: $BACKEND_URL"
echo "Frontend URL: $FRONTEND_URL"
echo ""
echo "📝 Next Steps:"
echo "1. Configure environment variables in Vercel dashboard"
echo "2. Update REACT_APP_API_URL to: $BACKEND_URL"
echo "3. Test the application"
echo ""
echo "🔧 Environment Variables to set in Vercel:"
echo "Backend:"
echo "- MONGODB_URL"
echo "- SENDGRID_API_KEY"
echo "- FROM_EMAIL"
echo "- FROM_NAME"
echo "- SECRET_KEY"
echo ""
echo "Frontend:"
echo "- REACT_APP_API_URL=$BACKEND_URL"
