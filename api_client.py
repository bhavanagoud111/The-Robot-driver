"""
API Client - Test client for the Cali Automation API
This demonstrates how to use the network-accessible automation service.
"""

import requests
import json
import time
import sys

API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test API health"""
    print("🏥 Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ API is healthy")
            print(f"📊 Services: {data.get('services', {})}")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on localhost:8000")
        return False

def test_core_automation():
    """Test core automation endpoint"""
    print("\n🤖 Testing Core Automation API...")
    try:
        payload = {
            "task_name": "Product Search Test",
            "description": "Search for products and report prices",
            "page_url": "https://books.toscrape.com/"
        }
        
        print(f"📤 Sending request: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{API_BASE_URL}/automate/core", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            task_id = data["task_id"]
            print(f"✅ Core automation started. Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ Core automation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Core automation error: {e}")
        return None

def test_ai_automation():
    """Test AI automation endpoint"""
    print("\n🧠 Testing AI Automation API...")
    try:
        payload = {
            "user_goal": "Find and click on the first book product",
            "page_url": "https://books.toscrape.com/"
        }
        
        print(f"📤 Sending request: {json.dumps(payload, indent=2)}")
        response = requests.post(f"{API_BASE_URL}/automate/ai", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            task_id = data["task_id"]
            print(f"✅ AI automation started. Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ AI automation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ AI automation error: {e}")
        return None

def check_task_status(task_id):
    """Check task status"""
    print(f"\n📊 Checking task {task_id} status...")
    try:
        response = requests.get(f"{API_BASE_URL}/tasks/{task_id}")
        
        if response.status_code == 200:
            data = response.json()
            status = data["status"]
            print(f"📋 Task Status: {status}")
            
            if status in ["completed", "failed"]:
                print(f"📝 Message: {data['message']}")
                if data.get("data", {}).get("result_data"):
                    result_data = data["data"]["result_data"]
                    if isinstance(result_data, dict):
                        print(f"📊 Result: {json.dumps(result_data, indent=2)}")
                    else:
                        print(f"📊 Result: {result_data}")
                return True
            else:
                print("⏳ Task still running...")
                return False
        else:
            print(f"❌ Failed to get task status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Task status check error: {e}")
        return False

def wait_for_completion(task_id, max_wait=60):
    """Wait for task completion"""
    print(f"⏳ Waiting for task {task_id} to complete (max {max_wait}s)...")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        if check_task_status(task_id):
            return True
        time.sleep(2)
    
    print(f"⏰ Task {task_id} did not complete within {max_wait} seconds")
    return False

def list_tasks():
    """List all tasks"""
    print("\n📋 Listing all tasks...")
    try:
        response = requests.get(f"{API_BASE_URL}/tasks")
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get("tasks", [])
            print(f"📊 Found {len(tasks)} tasks:")
            
            for task in tasks[:5]:  # Show first 5 tasks
                print(f"  - ID: {task['task_id']}, Name: {task['task_name']}, Status: {task['status']}")
            return True
        else:
            print(f"❌ Failed to list tasks: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ List tasks error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Cali Automation API Client Test")
    print("=" * 60)
    
    # Test API health
    if not test_api_health():
        print("❌ API is not available. Please start the API service first:")
        print("   python api_service_final.py")
        return 1
    
    print("\n" + "=" * 60)
    
    # Test core automation
    core_task_id = test_core_automation()
    if core_task_id:
        print(f"⏳ Waiting for core automation to complete...")
        wait_for_completion(core_task_id)
    
    print("\n" + "=" * 60)
    
    # Test AI automation
    ai_task_id = test_ai_automation()
    if ai_task_id:
        print(f"⏳ Waiting for AI automation to complete...")
        wait_for_completion(ai_task_id)
    
    print("\n" + "=" * 60)
    
    # List all tasks
    list_tasks()
    
    print("\n🎉 API client test completed!")
    print("=" * 60)
    print("📖 Visit http://localhost:8000/docs for interactive API documentation")
    print("🌐 API Endpoints:")
    print("   GET  / - API information")
    print("   GET  /health - Health check")
    print("   POST /automate/core - Core automation")
    print("   POST /automate/ai - AI automation")
    print("   GET  /tasks/{task_id} - Get task status")
    print("   GET  /tasks - List all tasks")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
