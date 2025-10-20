#!/usr/bin/env python3
"""
Simple test for web API
"""
import requests
import json
import time

def test_api():
    """Test the web API"""
    print("Testing Web API...")
    
    # Test the API
    response = requests.post(
        "http://localhost:8000/automate/goal",
        json={"user_goal": "find cheapest halloween dress"},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Response status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        task_id = response.json()["task_id"]
        print(f"Task ID: {task_id}")
        
        # Wait for completion
        print("Waiting for completion...")
        time.sleep(30)
        
        # Check result
        result_response = requests.get(f"http://localhost:8000/tasks/{task_id}")
        print(f"Result status: {result_response.status_code}")
        print(f"Result: {result_response.json()}")

if __name__ == "__main__":
    test_api()
