#!/usr/bin/env python3
"""
Deployment script for the Cali Automation Project
This script handles deployment and service management.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def print_header():
    """Print deployment header"""
    print("🚀 Cali Automation Project Deployment")
    print("=" * 50)
    print("Deploying web automation system")
    print("=" * 50)

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking deployment requirements...")
    
    # Check if setup was completed
    if not Path('requirements.txt').exists():
        print("❌ requirements.txt not found. Run setup.py first.")
        return False
    
    # Check if main files exist
    required_files = [
        'robot_driver_complete.py',
        'ai_brain_final.py',
        'api_service_simple.py'
    ]
    
    for file in required_files:
        if not Path(file).exists():
            print(f"❌ {file} not found")
            return False
    
    print("✅ All requirements met")
    return True

def start_api_service():
    """Start the API service"""
    print("\n🌐 Starting API service...")
    
    try:
        # Start the API service
        process = subprocess.Popen([
            sys.executable, 'api_service_simple.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ API service started successfully")
            print(f"🌐 API available at: http://localhost:8000")
            print(f"📖 Documentation: http://localhost:8000/docs")
            print(f"🔍 Health check: http://localhost:8000/health")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ API service failed to start")
            print(f"Error: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"❌ Failed to start API service: {e}")
        return None

def test_api_service():
    """Test the API service"""
    print("\n🧪 Testing API service...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API service is responding")
            return True
        else:
            print(f"❌ API service returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API service test failed: {e}")
        return False

def run_demo():
    """Run a demonstration"""
    print("\n🎬 Running demonstration...")
    
    try:
        # Run the API client test
        result = subprocess.run([sys.executable, 'api_client.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Demonstration completed successfully")
            print("📊 Check the output above for results")
        else:
            print("⚠️  Demonstration had some issues")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⚠️  Demonstration timed out")
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")

def print_deployment_info():
    """Print deployment information"""
    print("\n" + "="*60)
    print("🎉 Deployment Complete!")
    print("="*60)
    print("\n🌐 API Endpoints:")
    print("   GET  / - API information")
    print("   GET  /health - Health check")
    print("   POST /automate/core - Core automation")
    print("   POST /automate/ai - AI automation")
    print("   GET  /tasks/{task_id} - Get task status")
    print("   GET  /tasks - List all tasks")
    print("\n💡 Example Usage:")
    print("   curl -X POST 'http://localhost:8000/automate/core' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"task_name\": \"Product Search\"}'")
    print("\n📖 Visit http://localhost:8000/docs for interactive documentation")
    print("="*60)

def main():
    """Main deployment function"""
    print_header()
    
    # Check requirements
    if not check_requirements():
        print("❌ Deployment failed: Requirements not met")
        sys.exit(1)
    
    # Start API service
    process = start_api_service()
    if not process:
        print("❌ Deployment failed: Could not start API service")
        sys.exit(1)
    
    # Test API service
    if not test_api_service():
        print("❌ Deployment failed: API service not responding")
        process.terminate()
        sys.exit(1)
    
    # Print deployment info
    print_deployment_info()
    
    try:
        print("\n🎯 API service is running!")
        print("Press Ctrl+C to stop the service")
        
        # Keep the service running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping API service...")
        process.terminate()
        process.wait()
        print("✅ API service stopped")
    
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
