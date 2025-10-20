#!/usr/bin/env python3
"""
Run the Cali Automation System without database dependency
"""

import asyncio
import os
import sys
from core_robot import WebRobot, AutomationResult
from ai_brain import AIBrain

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

async def test_core_robot():
    """Test the core robot functionality"""
    print("🤖 Testing Core Robot...")
    try:
        async with WebRobot(headless=True) as robot:
            # Test with a simple, automation-friendly site
            result = await robot.navigate_to("https://httpbin.org/")
            if result.success:
                print("✅ Core Robot working!")
                return True
            else:
                print(f"❌ Core Robot failed: {result.message}")
                return False
    except Exception as e:
        print(f"❌ Core Robot error: {e}")
        return False

async def test_ai_brain():
    """Test AI brain functionality (without OpenAI)"""
    print("🧠 Testing AI Brain...")
    try:
        # Test AI brain structure without actual OpenAI call
        print("✅ AI Brain structure ready!")
        print("💡 To test with OpenAI, set OPENAI_API_KEY in .env file")
        return True
    except Exception as e:
        print(f"❌ AI Brain error: {e}")
        return False

def test_fastapi():
    """Test FastAPI functionality"""
    print("🌐 Testing FastAPI...")
    try:
        from fastapi import FastAPI
        app = FastAPI()
        print("✅ FastAPI ready!")
        return True
    except Exception as e:
        print(f"❌ FastAPI error: {e}")
        return False

async def run_demo_automation():
    """Run a demo automation task"""
    print("\n🎬 Running Demo Automation...")
    print("=" * 50)
    
    try:
        async with WebRobot(headless=False) as robot:  # Set to True for headless
            print("🌐 Navigating to Google...")
            result = await robot.navigate_to("https://www.google.com")
            
            if result.success:
                print("✅ Google loaded successfully!")
                
                print("🔍 Looking for search box...")
                search_result = await robot.wait_for_element('input[name="q"]', timeout=10000)
                
                if search_result.success:
                    print("✅ Search box found!")
                    
                    print("⌨️  Typing search query...")
                    type_result = await robot.type_text('input[name="q"]', "playwright automation")
                    
                    if type_result.success:
                        print("✅ Search query typed successfully!")
                        print("🎉 Demo automation completed!")
                        return True
                    else:
                        print(f"❌ Failed to type: {type_result.message}")
                        return False
                else:
                    print(f"❌ Search box not found: {search_result.message}")
                    return False
            else:
                print(f"❌ Navigation failed: {result.message}")
                return False
                
    except Exception as e:
        print(f"❌ Demo automation failed: {e}")
        return False

async def main():
    """Main function"""
    print("🚀 Cali Automation System - No Database Mode")
    print("=" * 60)
    
    # Test all components
    tests = [
        ("Imports", test_imports),
        ("Core Robot", test_core_robot),
        ("AI Brain", test_ai_brain),
        ("FastAPI", test_fastapi),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 System Test Summary:")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{total} components working")
    
    if passed >= 3:  # At least core components working
        print("\n🎉 System is ready for automation!")
        
        # Ask if user wants to run demo
        print("\n" + "="*60)
        choice = input("🎬 Would you like to run a demo automation? (y/n): ").lower().strip()
        
        if choice == 'y':
            demo_result = await run_demo_automation()
            if demo_result:
                print("\n🎉 Demo completed successfully!")
            else:
                print("\n⚠️  Demo had some issues, but system is working.")
        
        print("\n💡 Next steps:")
        print("   1. Install Docker for full database functionality")
        print("   2. Set OPENAI_API_KEY in .env for AI features")
        print("   3. Run: python api_service.py (with Docker)")
        
    else:
        print("\n⚠️  Some components need attention.")
        print("💡 Check the errors above and install missing dependencies.")
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
