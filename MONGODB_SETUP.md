# MongoDB Setup Guide for Citizen Issue Tracker

This guide will help you set up MongoDB for the Citizen Issue Tracker application on different operating systems.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Windows Setup](#windows-setup)
3. [macOS Setup](#macos-setup)
4. [Linux Setup](#linux-setup)
5. [Docker Setup](#docker-setup)
6. [MongoDB Atlas (Cloud)](#mongodb-atlas-cloud)
7. [Database Configuration](#database-configuration)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

- Administrative/sudo access to your system
- Internet connection for downloading MongoDB
- At least 1GB of free disk space

## Windows Setup

### Method 1: MongoDB Community Server (Recommended)

1. **Download MongoDB Community Server**
   - Go to [MongoDB Download Center](https://www.mongodb.com/try/download/community)
   - Select "Windows" as your platform
   - Choose "msi" package
   - Download the latest version

2. **Install MongoDB**
   - Run the downloaded `.msi` file
   - Choose "Complete" installation
   - Install MongoDB as a Windows Service
   - Install MongoDB Compass (optional but recommended)

3. **Start MongoDB Service**
   ```cmd
   # Open Command Prompt as Administrator
   net start MongoDB
   ```

4. **Verify Installation**
   ```cmd
   # Open Command Prompt
   mongo --version
   ```

### Method 2: Using Chocolatey

1. **Install Chocolatey** (if not already installed)
   ```powershell
   # Run PowerShell as Administrator
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install MongoDB**
   ```powershell
   choco install mongodb
   ```

3. **Start MongoDB**
   ```powershell
   net start MongoDB
   ```

## macOS Setup

### Method 1: Using Homebrew (Recommended)

1. **Install Homebrew** (if not already installed)
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Add MongoDB tap and install**
   ```bash
   brew tap mongodb/brew
   brew install mongodb-community
   ```

3. **Start MongoDB**
   ```bash
   brew services start mongodb/brew/mongodb-community
   ```

4. **Verify Installation**
   ```bash
   mongod --version
   ```

### Method 2: Manual Installation

1. **Download MongoDB**
   - Go to [MongoDB Download Center](https://www.mongodb.com/try/download/community)
   - Select "macOS" as your platform
   - Download the `.tgz` file

2. **Extract and Install**
   ```bash
   # Extract the downloaded file
   tar -zxvf mongodb-macos-x86_64-*.tgz
   
   # Move to /usr/local
   sudo mv mongodb-macos-x86_64-* /usr/local/mongodb
   
   # Add to PATH
   echo 'export PATH="/usr/local/mongodb/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Create data directory and start**
   ```bash
   sudo mkdir -p /usr/local/var/mongodb
   sudo chown $(whoami) /usr/local/var/mongodb
   mongod --dbpath /usr/local/var/mongodb
   ```

## Linux Setup

### Ubuntu/Debian

1. **Import MongoDB public key**
   ```bash
   wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
   ```

2. **Create list file**
   ```bash
   echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
   ```

3. **Update package database and install**
   ```bash
   sudo apt-get update
   sudo apt-get install -y mongodb-org
   ```

4. **Start MongoDB**
   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

5. **Verify Installation**
   ```bash
   mongod --version
   ```

### CentOS/RHEL/Fedora

1. **Create repo file**
   ```bash
   sudo vi /etc/yum.repos.d/mongodb-org-6.0.repo
   ```

2. **Add repository configuration**
   ```ini
   [mongodb-org-6.0]
   name=MongoDB Repository
   baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/6.0/x86_64/
   gpgcheck=1
   enabled=1
   gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
   ```

3. **Install MongoDB**
   ```bash
   sudo yum install -y mongodb-org
   # or for Fedora
   sudo dnf install -y mongodb-org
   ```

4. **Start MongoDB**
   ```bash
   sudo systemctl start mongod
   sudo systemctl enable mongod
   ```

## Docker Setup

### Using Docker Compose (Recommended)

1. **Create docker-compose.yml**
   ```yaml
   version: '3.8'
   services:
     mongodb:
       image: mongo:latest
       container_name: citizen-issue-tracker-mongodb
       restart: always
       ports:
         - "27017:27017"
       environment:
         MONGO_INITDB_ROOT_USERNAME: admin
         MONGO_INITDB_ROOT_PASSWORD: password123
         MONGO_INITDB_DATABASE: citizen_issue_tracker
       volumes:
         - mongodb_data:/data/db
         - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
   
   volumes:
     mongodb_data:
   ```

2. **Create mongo-init.js** (optional)
   ```javascript
   db = db.getSiblingDB('citizen_issue_tracker');
   
   // Create collections
   db.createCollection('users');
   db.createCollection('issues');
   
   // Create indexes
   db.users.createIndex({ "email": 1 }, { unique: true });
   db.issues.createIndex({ "reported_by": 1 });
   db.issues.createIndex({ "status": 1 });
   db.issues.createIndex({ "category": 1 });
   db.issues.createIndex({ "created_at": -1 });
   ```

3. **Start MongoDB**
   ```bash
   docker-compose up -d
   ```

### Using Docker Run

1. **Run MongoDB container**
   ```bash
   docker run -d \
     --name citizen-issue-tracker-mongodb \
     -p 27017:27017 \
     -e MONGO_INITDB_ROOT_USERNAME=admin \
     -e MONGO_INITDB_ROOT_PASSWORD=password123 \
     -v mongodb_data:/data/db \
     mongo:latest
   ```

2. **Connect to MongoDB**
   ```bash
   docker exec -it citizen-issue-tracker-mongodb mongo
   ```

## MongoDB Atlas (Cloud)

1. **Create Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/atlas)
   - Sign up for a free account

2. **Create Cluster**
   - Click "Build a Database"
   - Choose "FREE" tier (M0)
   - Select your preferred cloud provider and region
   - Give your cluster a name
   - Click "Create"

3. **Configure Access**
   - Go to "Database Access" in the left sidebar
   - Click "Add New Database User"
   - Create a username and password
   - Give "Atlas admin" privileges

4. **Network Access**
   - Go to "Network Access" in the left sidebar
   - Click "Add IP Address"
   - Add your current IP or use "0.0.0.0/0" for all IPs (less secure)

5. **Get Connection String**
   - Go to "Database" in the left sidebar
   - Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password

6. **Update Environment Variables**
   ```env
   MONGODB_URL=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/citizen_issue_tracker?retryWrites=true&w=majority
   ```

## Database Configuration

### Connection String Format

**Local MongoDB:**
```
mongodb://localhost:27017/citizen_issue_tracker
```

**MongoDB with Authentication:**
```
mongodb://username:password@localhost:27017/citizen_issue_tracker
```

**MongoDB Atlas:**
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/citizen_issue_tracker?retryWrites=true&w=majority
```

### Environment Variables

Create a `.env` file in the backend directory:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=citizen_issue_tracker

# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database Collections

The application will automatically create these collections:

- **users**: User accounts and profiles
- **issues**: Reported issues and their details
- **sessions**: User sessions (if using session-based auth)

### Indexes

The application will create these indexes for better performance:

```javascript
// Users collection
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "role": 1 });

// Issues collection
db.issues.createIndex({ "reported_by": 1 });
db.issues.createIndex({ "status": 1 });
db.issues.createIndex({ "category": 1 });
db.issues.createIndex({ "priority": 1 });
db.issues.createIndex({ "created_at": -1 });
db.issues.createIndex({ "assigned_to": 1 });
```

## Troubleshooting

### Common Issues

1. **MongoDB won't start**
   ```bash
   # Check if port 27017 is in use
   netstat -an | grep 27017
   
   # Kill process using the port
   sudo lsof -ti:27017 | xargs kill -9
   ```

2. **Permission denied errors**
   ```bash
   # Fix data directory permissions
   sudo chown -R mongodb:mongodb /var/lib/mongodb
   sudo chown -R mongodb:mongodb /var/log/mongodb
   ```

3. **Connection refused**
   - Ensure MongoDB is running
   - Check firewall settings
   - Verify connection string

4. **Authentication failed**
   - Check username and password
   - Ensure user has proper permissions
   - Verify database name

### Logs

**Windows:**
- Event Viewer → Windows Logs → Application
- Look for MongoDB entries

**macOS/Linux:**
```bash
# Check MongoDB logs
sudo tail -f /var/log/mongodb/mongod.log

# Or if using Homebrew on macOS
tail -f /usr/local/var/log/mongodb/mongo.log
```

### Testing Connection

1. **Using MongoDB Shell**
   ```bash
   mongo
   # or
   mongosh
   ```

2. **Using Python**
   ```python
   from pymongo import MongoClient
   
   client = MongoClient('mongodb://localhost:27017/')
   db = client['citizen_issue_tracker']
   print(db.list_collection_names())
   ```

3. **Using Node.js**
   ```javascript
   const { MongoClient } = require('mongodb');
   
   async function testConnection() {
     const client = new MongoClient('mongodb://localhost:27017/');
     await client.connect();
     console.log('Connected to MongoDB');
     await client.close();
   }
   
   testConnection();
   ```

## Security Best Practices

1. **Enable Authentication**
   ```bash
   # Create admin user
   mongo
   use admin
   db.createUser({
     user: "admin",
     pwd: "secure_password",
     roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
   })
   ```

2. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix of letters, numbers, and symbols
   - Avoid common words

3. **Network Security**
   - Use VPN for remote access
   - Whitelist specific IP addresses
   - Use SSL/TLS encryption

4. **Regular Backups**
   ```bash
   # Create backup
   mongodump --db citizen_issue_tracker --out /backup/path
   
   # Restore backup
   mongorestore --db citizen_issue_tracker /backup/path/citizen_issue_tracker
   ```

## Next Steps

After setting up MongoDB:

1. Update your `.env` file with the correct connection string
2. Start the backend application
3. Verify the connection in the application logs
4. Test the API endpoints

For any issues, check the troubleshooting section or refer to the [MongoDB documentation](https://docs.mongodb.com/).
