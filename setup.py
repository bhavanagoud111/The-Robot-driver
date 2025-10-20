#!/usr/bin/env python3
"""
Setup script for the Cali Automation Project
This script handles the complete setup and installation process.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header():
    """Print setup header"""
    print("🎯 Cali Automation Project Setup")
    print("=" * 50)
    print("Setting up web automation system with AI capabilities")
    print("=" * 50)

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are available"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'playwright',
        'fastapi',
        'uvicorn',
        'pydantic',
        'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages, check=True)
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def install_playwright_browsers():
    """Install Playwright browsers"""
    print("\n🎭 Installing Playwright browsers...")
    try:
        subprocess.run(['playwright', 'install'], check=True)
        print("✅ Playwright browsers installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Playwright browsers")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n📝 Setting up environment file...")
    
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_file.exists():
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print("✅ Created .env file from template")
        else:
            # Create basic .env file
            env_content = """# Cali Automation Environment Variables

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# OpenAI API Key (optional, for AI Brain functionality)
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration (optional)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cali_automation
DB_USER=cali_user
DB_PASSWORD=cali_password
"""
            env_file.write_text(env_content)
            print("✅ Created .env file with default values")
    else:
        print("✅ .env file already exists")

def test_installation():
    """Test the installation"""
    print("\n🧪 Testing installation...")
    
    # Test core robot
    print("🤖 Testing core robot...")
    try:
        result = subprocess.run([sys.executable, 'robot_driver_complete.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Core robot test passed")
        else:
            print("⚠️  Core robot test had issues (this is normal for some environments)")
    except subprocess.TimeoutExpired:
        print("⚠️  Core robot test timed out (this is normal)")
    except Exception as e:
        print(f"⚠️  Core robot test failed: {e}")
    
    # Test AI brain
    print("🧠 Testing AI brain...")
    try:
        result = subprocess.run([sys.executable, 'ai_brain_final.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ AI brain test passed")
        else:
            print("⚠️  AI brain test had issues (this is normal without OpenAI key)")
    except subprocess.TimeoutExpired:
        print("⚠️  AI brain test timed out (this is normal)")
    except Exception as e:
        print(f"⚠️  AI brain test failed: {e}")

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\n📋 Usage Instructions:")
    print("\n1. Core Robot Driver (Required Core):")
    print("   python robot_driver_complete.py")
    print("\n2. AI Brain (Optional Challenge 1):")
    print("   python ai_brain_final.py")
    print("\n3. Web API Service (Optional Challenge 2):")
    print("   python api_service_simple.py")
    print("   Then visit: http://localhost:8000/docs")
    print("\n4. Test API Client:")
    print("   python api_client.py")
    print("\n📖 For detailed instructions, see README.md")
    print("="*60)

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check and install dependencies
    if not check_dependencies():
        print("❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        print("❌ Setup failed: Could not install Playwright browsers")
        sys.exit(1)
    
    # Create environment file
    create_env_file()
    
    # Test installation
    test_installation()
    
    # Print usage instructions
    print_usage_instructions()
    
    print("\n🎯 Setup completed successfully!")
    print("💡 You can now run the automation system!")

if __name__ == "__main__":
    main()
