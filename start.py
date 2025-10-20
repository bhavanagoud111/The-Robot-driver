#!/usr/bin/env python3
"""
Startup script for the Cali Automation System
"""

import os
import sys
import subprocess
import time
from dotenv import load_dotenv

def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def start_database():
    """Start the MySQL database"""
    print("🐳 Starting MySQL database...")
    try:
        subprocess.run(['docker-compose', 'up', '-d'], check=True)
        print("✅ Database started successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start database: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("📦 Checking dependencies...")
    try:
        import playwright
        import fastapi
        import sqlalchemy
        import openai
        print("✅ All dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def install_playwright():
    """Install Playwright browsers"""
    print("🎭 Installing Playwright browsers...")
    try:
        subprocess.run(['playwright', 'install'], check=True)
        print("✅ Playwright browsers installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Playwright browsers: {e}")
        return False

def initialize_database():
    """Initialize the database"""
    print("🗄️  Initializing database...")
    try:
        from database import init_database
        init_database()
        print("✅ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize database: {e}")
        return False

def start_api():
    """Start the API service"""
    print("🚀 Starting API service...")
    try:
        import uvicorn
        from api_service import app
        
        host = os.getenv('API_HOST', '0.0.0.0')
        port = int(os.getenv('API_PORT', 8000))
        
        print(f"🌐 API will be available at: http://{host}:{port}")
        print(f"📖 API Documentation: http://{host}:{port}/docs")
        print("Press Ctrl+C to stop the server")
        
        uvicorn.run(app, host=host, port=port)
    except KeyboardInterrupt:
        print("\n👋 API service stopped")
    except Exception as e:
        print(f"❌ Failed to start API service: {e}")

def main():
    """Main startup function"""
    print("🎯 Cali Automation System Startup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  .env file not found. Please copy env.example to .env and configure it.")
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check Docker
    if not check_docker():
        print("❌ Docker is not running. Please start Docker and try again.")
        return 1
    
    # Start database
    if not start_database():
        return 1
    
    # Wait for database to be ready
    print("⏳ Waiting for database to be ready...")
    time.sleep(5)
    
    # Initialize database
    if not initialize_database():
        return 1
    
    # Install Playwright browsers
    if not install_playwright():
        return 1
    
    print("\n🎉 System is ready!")
    print("=" * 50)
    print("Available commands:")
    print("  python core_robot.py     - Run core automation")
    print("  python ai_brain.py       - Run AI automation")
    print("  python test_system.py    - Run system tests")
    print("  python start.py          - Start API service")
    print("=" * 50)
    
    # Ask user what to do
    choice = input("\nWhat would you like to do? (api/test/core/ai/quit): ").lower().strip()
    
    if choice == 'api':
        start_api()
    elif choice == 'test':
        print("🧪 Running system tests...")
        subprocess.run([sys.executable, 'test_system.py'])
    elif choice == 'core':
        print("🤖 Running core automation...")
        subprocess.run([sys.executable, 'core_robot.py'])
    elif choice == 'ai':
        print("🧠 Running AI automation...")
        subprocess.run([sys.executable, 'ai_brain.py'])
    elif choice == 'quit':
        print("👋 Goodbye!")
    else:
        print("Invalid choice. Please run the script again.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
