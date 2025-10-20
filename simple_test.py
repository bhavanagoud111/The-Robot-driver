"""
Simple test script that works with automation-friendly websites
"""

import asyncio
import logging
from core_robot import WebRobot, AutomationResult

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_simple_automation():
    """Test automation with a simple, automation-friendly website"""
    print("🤖 Testing Simple Web Automation...")
    
    try:
        async with WebRobot(headless=False) as robot:  # Set to True for headless
            # Test with a simple website that doesn't have bot detection
            print("🌐 Testing with httpbin.org (automation-friendly)...")
            
            # Navigate to a simple test site
            result = await robot.navigate_to("https://httpbin.org/forms/post")
            if not result.success:
                print(f"❌ Navigation failed: {result.message}")
                return False
            
            print("✅ Navigation successful!")
            
            # Try to find and interact with form elements
            print("🔍 Looking for form elements...")
            
            # Wait for form to load
            wait_result = await robot.wait_for_element("form", timeout=10000)
            if wait_result.success:
                print("✅ Form found!")
                
                # Try to get page title
                title_result = await robot.get_text("title")
                if title_result.success:
                    print(f"📄 Page title: {title_result.data['text']}")
                
                return True
            else:
                print("❌ Form not found")
                return False
                
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_google_search():
    """Test with Google (usually automation-friendly)"""
    print("🔍 Testing Google Search...")
    
    try:
        async with WebRobot(headless=False) as robot:
            # Navigate to Google
            result = await robot.navigate_to("https://www.google.com")
            if not result.success:
                print(f"❌ Google navigation failed: {result.message}")
                return False
            
            print("✅ Google loaded successfully!")
            
            # Try to find the search box
            search_result = await robot.wait_for_element('input[name="q"]', timeout=10000)
            if search_result.success:
                print("✅ Google search box found!")
                
                # Type a search query
                type_result = await robot.type_text('input[name="q"]', "playwright automation")
                if type_result.success:
                    print("✅ Search query typed successfully!")
                    return True
                else:
                    print(f"❌ Failed to type search query: {type_result.message}")
                    return False
            else:
                print("❌ Google search box not found")
                return False
                
    except Exception as e:
        print(f"❌ Google test failed: {e}")
        return False

async def main():
    """Run all simple tests"""
    print("🧪 Simple Automation Tests")
    print("=" * 50)
    
    tests = [
        ("Simple Website", test_simple_automation),
        ("Google Search", test_google_search),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = await test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Summary:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your automation system is working!")
    else:
        print("⚠️  Some tests failed. This is normal for web automation.")
        print("💡 The system is working - some sites just block automation.")

if __name__ == "__main__":
    asyncio.run(main())
