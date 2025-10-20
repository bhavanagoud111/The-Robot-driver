#!/usr/bin/env python3
"""
Debug script for automation
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_automation import UniversalAutomation

async def debug_automation():
    """Debug the automation system"""
    print("Debugging Universal Automation...")
    
    automation = UniversalAutomation()
    
    try:
        # Test browser startup
        print("Testing browser startup...")
        browser_started = await automation.start_browser()
        print(f"Browser started: {browser_started}")
        
        if browser_started:
            print("Testing automation execution...")
            result = await automation.execute_automation("find cheapest halloween dress")
            print(f"Result type: {type(result)}")
            print(f"Result: {result}")
            
            if hasattr(result, 'success'):
                print(f"Success: {result.success}")
                print(f"Message: {result.message}")
                print(f"Data: {result.data}")
            elif isinstance(result, dict):
                print(f"Dict - Success: {result.get('success')}")
                print(f"Dict - Message: {result.get('message')}")
                print(f"Dict - Data: {result.get('data')}")
            else:
                print(f"Unknown result type: {type(result)}")
        else:
            print("Failed to start browser")
            
    except Exception as e:
        print(f"Error during debugging: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            await automation.close_browser()
        except:
            pass

if __name__ == "__main__":
    asyncio.run(debug_automation())
