#!/bin/bash

# Cali Automation - Automated Setup Script
# This script sets up the complete Cali Automation system

set -e  # Exit on any error

echo "🚀 Cali Automation - Automated Setup"
echo "====================================="

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.8 or higher is required. Found: $python_version"
    exit 1
fi
echo "✅ Python version: $python_version"

# Check if pip is available
echo "📋 Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed. Please install pip first."
    exit 1
fi
echo "✅ pip3 is available"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo "✅ Created .env file (you can edit it later)"
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
echo "🔧 Setting up permissions..."
chmod +x setup.sh
chmod +x start_web_interface.py

# Test installation
echo "🧪 Testing installation..."
python3 -c "
import playwright
import fastapi
import uvicorn
print('✅ All required packages are installed')
"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🚀 To start the system (two terminals):"
echo "   python3 web_api.py"
echo "   python3 start_web_interface.py"
echo ""
echo "🌐 Access points:"
echo "   Web Interface: http://localhost:8081"
echo "   API Server: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📖 For detailed instructions, see SETUP.md"
echo ""
echo "🎯 Ready to automate anything!"