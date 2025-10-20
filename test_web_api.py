#!/usr/bin/env python3
"""
Test script for web API automation
"""
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from universal_automation import UniversalAutomation

async def test_web_api_automation():
    """Test the automation as it would be called from web API"""
    print("Testing Web API Automation...")
    
    try:
        from universal_automation import UniversalAutomation
        
        # Create Universal Automation instance
        automation = UniversalAutomation()
        
        # Execute universal automation
        print("Running Universal Automation...")
        result = await automation.execute_automation("find cheapest halloween dress", "https://duckduckgo.com")
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        
        # Check if result is valid
        if result is None:
            print("ERROR: Automation returned None result")
            return
        
        # Process automation result
        # Handle both AutomationResult object and dictionary
        if hasattr(result, 'success'):
            success = result.success
            message = result.message
            data = result.data
            error = result.error
            print(f"Processing AutomationResult: success={success}, message={message}")
        elif isinstance(result, dict):
            success = result.get('success', False)
            message = result.get('message', 'Unknown result')
            data = result.get('data', {})
            error = result.get('error', None)
            print(f"Processing dict: success={success}, message={message}")
        else:
            print(f"ERROR: Unknown result type: {type(result)}")
            return
        
        if success:
            print("SUCCESS: Automation completed successfully")
            print(f"Data: {data}")
        else:
            print(f"FAILED: {message}")
            print(f"Error: {error}")
            
    except Exception as e:
        print(f"Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_web_api_automation())
