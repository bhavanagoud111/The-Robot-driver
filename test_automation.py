#!/usr/bin/env python3
"""
Test script for universal automation
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_automation import UniversalAutomation

async def test_automation():
    """Test the automation system"""
    print("Testing Universal Automation...")
    
    automation = UniversalAutomation()
    
    try:
        # Test browser startup
        print("Testing browser startup...")
        browser_started = await automation.start_browser()
        print(f"Browser started: {browser_started}")
        
        if browser_started:
            print("Testing automation execution...")
            result = await automation.execute_automation("find cheapest halloween dress")
            print(f"Automation result: {result}")
            print(f"Success: {result.success if result else 'None'}")
            print(f"Message: {result.message if result else 'None'}")
        else:
            print("Failed to start browser")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            await automation.close_browser()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(test_automation())
