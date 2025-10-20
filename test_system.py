"""
Test script to verify the automation system functionality
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_core_robot():
    """Test the core robot functionality"""
    print("🤖 Testing Core Robot...")
    try:
        from core_robot import ExampleTask
        
        task = ExampleTask()
        result = await task.execute_example_task()
        
        if result.success:
            print(f"✅ Core Robot Test Passed: {result.message}")
            return True
        else:
            print(f"❌ Core Robot Test Failed: {result.message}")
            return False
    except Exception as e:
        print(f"❌ Core Robot Test Error: {e}")
        return False

async def test_ai_brain():
    """Test the AI brain functionality"""
    print("🧠 Testing AI Brain...")
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("⚠️  OpenAI API key not found. Skipping AI Brain test.")
            return True
        
        from ai_brain import AIBrain
        
        ai_brain = AIBrain(api_key)
        result = await ai_brain.execute_ai_task(
            user_goal="Find the search box and type 'laptop'",
            page_url="https://demo.opencart.com/"
        )
        
        if result.success:
            print(f"✅ AI Brain Test Passed: {result.message}")
            return True
        else:
            print(f"❌ AI Brain Test Failed: {result.message}")
            return False
    except Exception as e:
        print(f"❌ AI Brain Test Error: {e}")
        return False

def test_database():
    """Test database connection"""
    print("🗄️  Testing Database...")
    try:
        from database import init_database, get_db, AutomationTask
        
        # Initialize database
        init_database()
        
        # Test database connection
        db = next(get_db())
        task_count = db.query(AutomationTask).count()
        print(f"✅ Database Test Passed: {task_count} tasks found")
        return True
    except Exception as e:
        print(f"❌ Database Test Failed: {e}")
        return False

def test_imports():
    """Test that all modules can be imported"""
    print("📦 Testing Imports...")
    try:
        import playwright
        import fastapi
        import sqlalchemy
        import openai
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🧪 Starting System Tests...\n")
    
    tests = [
        ("Imports", test_imports),
        ("Database", test_database),
        ("Core Robot", test_core_robot),
        ("AI Brain", test_ai_brain),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"{'='*50}")
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
        print()
    
    # Summary
    print("="*50)
    print("📊 Test Summary:")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
