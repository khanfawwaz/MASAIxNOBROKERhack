#!/usr/bin/env python3
"""
Citizen Issue Tracker Setup Script
This script helps set up the development environment for the Citizen Issue Tracker.
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def run_command(command, shell=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_requirements():
    """Check if required software is installed."""
    print("🔍 Checking requirements...")
    
    requirements = {
        "Node.js": "node --version",
        "Python": "python --version",
        "MongoDB": "mongod --version"
    }
    
    missing = []
    
    for name, command in requirements.items():
        success, stdout, stderr = run_command(command)
        if success:
            version = stdout.strip().split('\n')[0]
            print(f"✅ {name}: {version}")
        else:
            print(f"❌ {name}: Not found")
            missing.append(name)
    
    return missing

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    
    # Install root dependencies
    print("Installing root dependencies...")
    success, stdout, stderr = run_command("npm install")
    if not success:
        print(f"❌ Failed to install root dependencies: {stderr}")
        return False
    
    # Install frontend dependencies
    print("Installing frontend dependencies...")
    os.chdir("frontend")
    success, stdout, stderr = run_command("npm install")
    if not success:
        print(f"❌ Failed to install frontend dependencies: {stderr}")
        return False
    
    # Install backend dependencies
    print("Installing backend dependencies...")
    os.chdir("../backend")
    success, stdout, stderr = run_command("pip install -r requirements.txt")
    if not success:
        print(f"❌ Failed to install backend dependencies: {stderr}")
        return False
    
    os.chdir("..")
    print("✅ All dependencies installed successfully!")
    return True

def setup_environment():
    """Set up environment variables."""
    print("\n🔧 Setting up environment...")
    
    env_file = Path("backend/.env")
    env_example = Path("backend/env.example")
    
    if not env_file.exists() and env_example.exists():
        # Copy example to .env
        with open(env_example, 'r') as f:
            content = f.read()
        
        with open(env_file, 'w') as f:
            f.write(content)
        
        print("✅ Environment file created from example")
    else:
        print("ℹ️  Environment file already exists")
    
    return True

def setup_mongodb():
    """Set up MongoDB."""
    print("\n🗄️  Setting up MongoDB...")
    
    system = platform.system().lower()
    
    if system == "windows":
        print("Starting MongoDB service on Windows...")
        success, stdout, stderr = run_command("net start MongoDB")
        if not success:
            print("❌ Failed to start MongoDB. Please start it manually.")
            print("Run: net start MongoDB")
            return False
    elif system == "darwin":  # macOS
        print("Starting MongoDB service on macOS...")
        success, stdout, stderr = run_command("brew services start mongodb/brew/mongodb-community")
        if not success:
            print("❌ Failed to start MongoDB. Please start it manually.")
            print("Run: brew services start mongodb/brew/mongodb-community")
            return False
    elif system == "linux":
        print("Starting MongoDB service on Linux...")
        success, stdout, stderr = run_command("sudo systemctl start mongod")
        if not success:
            print("❌ Failed to start MongoDB. Please start it manually.")
            print("Run: sudo systemctl start mongod")
            return False
    else:
        print("❌ Unsupported operating system. Please start MongoDB manually.")
        return False
    
    print("✅ MongoDB is running!")
    return True

def create_sample_data():
    """Create sample data for testing."""
    print("\n📝 Creating sample data...")
    
    # This would typically create sample users and issues
    # For now, we'll just print instructions
    print("ℹ️  Sample data creation not implemented yet.")
    print("You can create test accounts through the web interface.")
    
    return True

def main():
    """Main setup function."""
    print("🚀 Citizen Issue Tracker Setup")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("package.json").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check requirements
    missing = check_requirements()
    if missing:
        print(f"\n❌ Missing requirements: {', '.join(missing)}")
        print("Please install the missing software and run this script again.")
        print("\nInstallation guides:")
        print("- Node.js: https://nodejs.org/")
        print("- Python: https://python.org/")
        print("- MongoDB: See MONGODB_SETUP.md")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        print("❌ Failed to setup environment")
        sys.exit(1)
    
    # Setup MongoDB
    if not setup_mongodb():
        print("❌ Failed to setup MongoDB")
        sys.exit(1)
    
    # Create sample data
    create_sample_data()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: npm run dev")
    print("2. Open: http://localhost:3000")
    print("3. Create your first account")
    print("\nFor detailed instructions, see QUICK_START.md")

if __name__ == "__main__":
    main()
