# 🚀 Cali Automation - Complete Setup Guide

## Overview
Cali Automation is an AI-powered web automation system that can perform any task you give it. It uses Playwright for browser automation, FastAPI for the web service, and intelligent AI planning for dynamic task execution.

## ✨ Features
- **Universal Automation** - Works with any type of goal (shopping, news, jobs, travel, etc.)
- **AI-Powered Planning** - Intelligently determines the best website and automation strategy
- **Real Browser Automation** - Opens visible browser windows and performs actual tasks
- **Web Interface** - Easy-to-use web interface for submitting goals
- **REST API** - Programmatic access to automation capabilities

## 🛠️ Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

## 📦 Installation

### Step 1: Clone or Download the Project
```bash
# If you have git:
git clone <repository-url>
cd cali-project

# Or download and extract the project files to a folder
```

### Step 2: Install Python Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### Step 3: Set Up Environment (Optional)
```bash
# Copy environment template
cp env.example .env

# Edit .env file with your settings (optional)
# OPENAI_API_KEY=your_openai_key_here  # For enhanced AI features
```

## 🚀 Running the System

### Method 1: Quick Start (Recommended)
```bash
# Start the complete system
python start_web_interface.py
```
This will start both the API server and web interface automatically.

### Method 2: Manual Start
```bash
# Terminal 1: Start API Server
python web_api.py

# Terminal 2: Start Web Interface  
python start_web_interface.py
```

## 🌐 Access Points

### Web Interface
- **URL:** http://localhost:8081
- **Purpose:** User-friendly interface to submit automation goals
- **Features:** 
  - Type any goal in plain English
  - Watch real-time automation progress
  - View detailed results with clickable links

### API Endpoints
- **Base URL:** http://localhost:8000
- **Health Check:** http://localhost:8000/health
- **API Docs:** http://localhost:8000/docs

#### Key API Endpoints:
- `POST /automate/goal` - Submit automation goals
- `GET /tasks/{task_id}` - Check task status and results
- `GET /tasks` - List all tasks

## 📝 Usage Examples

### Web Interface Usage
1. Open http://localhost:8081 in your browser
2. Type your goal (e.g., "Find the best laptop deals under $1000")
3. Click "🚀 Start AI Automation"
4. Watch the browser open and perform the automation
5. View the results with clickable links

### API Usage
```bash
# Submit a goal
curl -X POST "http://localhost:8000/automate/goal" \
  -H "Content-Type: application/json" \
  -d '{"user_goal": "find cheapest halloween dress"}'

# Check results
curl "http://localhost:8000/tasks/{task_id}"
```

### Example Goals to Try
- "Find the best laptop deals under $1000"
- "Search for flights from New York to London"
- "Find job openings for software engineer"
- "Get the latest news about AI technology"
- "Find restaurants near me with good reviews"
- "Search for Python programming tutorials"

## 🔧 Configuration

### Environment Variables (.env file)
```bash
# Optional: OpenAI API Key for enhanced AI features
OPENAI_API_KEY=your_openai_key_here

# Optional: Database settings
DB_HOST=localhost
DB_PORT=3306
DB_USER=cali_user
DB_PASSWORD=cali_password
DB_NAME=cali_automation

# Optional: API settings
API_HOST=0.0.0.0
API_PORT=8000
WEB_PORT=8081
```

### Website Selection Logic
The system automatically selects the best website based on your goal:
- **Shopping queries** → DuckDuckGo (finds deals across multiple sites)
- **News/Research** → DuckDuckGo
- **Job searches** → LinkedIn Jobs
- **Travel queries** → Skyscanner
- **Video/Tutorials** → YouTube
- **Restaurants** → Google Maps
- **Books** → Books.toscrape.com

## 🐛 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Kill existing processes
pkill -f web_api.py
pkill -f start_web_interface.py

# Or use different ports
export API_PORT=8001
export WEB_PORT=8082
```

#### 2. Playwright Browser Issues
```bash
# Reinstall browsers
playwright install --force

# Install specific browser
playwright install chromium
```

#### 3. Permission Issues
```bash
# Make scripts executable
chmod +x setup.sh
chmod +x start_web_interface.py
```

#### 4. Python Path Issues
```bash
# Use full path to Python
/usr/bin/python3 web_api.py
# or
python3 -m pip install -r requirements.txt
```

### Logs and Debugging
- Check terminal output for error messages
- API logs are displayed in the terminal running `web_api.py`
- Web interface logs are displayed in the terminal running `start_web_interface.py`

## 📁 Project Structure
```
cali-project/
├── web_api.py                    # Main API server
├── ai_brain_mcp_integration.py   # AI Brain with MCP integration
├── goal_interface.html           # Web interface
├── start_web_interface.py        # Web server launcher
├── requirements.txt              # Python dependencies
├── env.example                  # Environment template
├── SETUP.md                     # This file
└── README.md                    # Project overview
```

## 🔄 Development

### Adding New Features
1. Modify `ai_brain_mcp_integration.py` for automation logic
2. Update `web_api.py` for new API endpoints
3. Enhance `goal_interface.html` for UI improvements

### Testing
```bash
# Test API endpoints
python -c "
import requests
response = requests.post('http://localhost:8000/automate/goal', 
                        json={'user_goal': 'test query'})
print(response.json())
"

# Test web interface
curl http://localhost:8081
```

## 🚀 Deployment

### Local Development
- Use the setup above for local development and testing

### Production Deployment
1. Set up a web server (nginx, Apache)
2. Use a process manager (PM2, systemd)
3. Configure SSL certificates
4. Set up monitoring and logging

### Docker Deployment (Optional)
```bash
# Build Docker image
docker build -t cali-automation .

# Run container
docker run -p 8000:8000 -p 8081:8081 cali-automation
```

## 📞 Support

### Getting Help
1. Check the troubleshooting section above
2. Review terminal logs for error messages
3. Test individual components (API, web interface, automation)

### System Requirements
- **Minimum:** 2GB RAM, 1 CPU core
- **Recommended:** 4GB RAM, 2 CPU cores
- **Browser:** Chrome, Firefox, or Safari for web interface

## 🎉 Success Indicators

You'll know the system is working when:
1. ✅ API server starts without errors on port 8000
2. ✅ Web interface loads on port 8081
3. ✅ Browser opens when you submit a goal
4. ✅ Search results appear with clickable links
5. ✅ Results are relevant to your query

---

**🎯 Ready to automate anything!** Open http://localhost:8081 and start exploring the power of AI-driven web automation.