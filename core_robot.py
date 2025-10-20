"""
Core Robot Driver - Foundational web automation using Playwright
This module provides the basic automation capabilities for web tasks.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AutomationResult:
    """Result of an automation task"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class WebRobot:
    """Core web automation robot using Playwright"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def start(self):
        """Start the browser and create a new page"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            self.page = await self.context.new_page()
            logger.info("Browser started successfully")
        except Exception as e:
            logger.error(f"Failed to start browser: {e}")
            raise
    
    async def close(self):
        """Close the browser and cleanup"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def navigate_to(self, url: str, timeout: int = 30000) -> AutomationResult:
        """Navigate to a URL with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Navigating to: {url}")
            await self.page.goto(url, timeout=timeout, wait_until='domcontentloaded')
            
            # Wait for page to be ready
            await self.page.wait_for_load_state('networkidle', timeout=timeout)
            
            return AutomationResult(
                success=True,
                message=f"Successfully navigated to {url}",
                data={'url': url, 'title': await self.page.title()}
            )
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return AutomationResult(
                success=False,
                message=f"Failed to navigate to {url}",
                error=str(e)
            )
    
    async def click_element(self, selector: str, timeout: int = 10000) -> AutomationResult:
        """Click an element by selector with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Clicking element: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            
            return AutomationResult(
                success=True,
                message=f"Successfully clicked element: {selector}"
            )
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return AutomationResult(
                success=False,
                message=f"Failed to click element: {selector}",
                error=str(e)
            )
    
    async def type_text(self, selector: str, text: str, timeout: int = 10000) -> AutomationResult:
        """Type text into an element with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Typing text into: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, text)
            
            return AutomationResult(
                success=True,
                message=f"Successfully typed text into: {selector}"
            )
        except Exception as e:
            logger.error(f"Type text failed: {e}")
            return AutomationResult(
                success=False,
                message=f"Failed to type text into: {selector}",
                error=str(e)
            )
    
    async def get_text(self, selector: str, timeout: int = 10000) -> AutomationResult:
        """Get text content from an element"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Getting text from: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            text = await self.page.text_content(selector)
            
            return AutomationResult(
                success=True,
                message=f"Successfully retrieved text from: {selector}",
                data={'text': text}
            )
        except Exception as e:
            logger.error(f"Get text failed: {e}")
            return AutomationResult(
                success=False,
                message=f"Failed to get text from: {selector}",
                error=str(e)
            )
    
    async def wait_for_element(self, selector: str, timeout: int = 10000) -> AutomationResult:
        """Wait for an element to appear"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Waiting for element: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            
            return AutomationResult(
                success=True,
                message=f"Element found: {selector}"
            )
        except Exception as e:
            logger.error(f"Wait for element failed: {e}")
            return AutomationResult(
                success=False,
                message=f"Element not found: {selector}",
                error=str(e)
            )

class ExampleTask:
    """Example automation task: Login and search for a product"""
    
    def __init__(self):
        self.robot = WebRobot(headless=False)  # Set to True for headless mode
    
    async def execute_example_task(self) -> AutomationResult:
        """Execute a complete example task"""
        try:
            async with self.robot as robot:
                # Navigate to a demo e-commerce site
                nav_result = await robot.navigate_to("https://demo.opencart.com/")
                if not nav_result.success:
                    return nav_result
                
                # Search for a product
                search_result = await robot.type_text(
                    'input[name="search"]', 
                    "laptop"
                )
                if not search_result.success:
                    return search_result
                
                # Click search button
                click_result = await robot.click_element('button[type="submit"]')
                if not click_result.success:
                    return click_result
                
                # Wait for results and get first product name
                await robot.wait_for_element('.product-thumb', timeout=15000)
                product_result = await robot.get_text('.product-thumb h4 a')
                
                if product_result.success:
                    return AutomationResult(
                        success=True,
                        message=f"Success! Found product: {product_result.data['text']}",
                        data={'product_name': product_result.data['text']}
                    )
                else:
                    return AutomationResult(
                        success=False,
                        message="Product search completed but no product found",
                        error="No products found in search results"
                    )
                    
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return AutomationResult(
                success=False,
                message="Task execution failed",
                error=str(e)
            )

async def main():
    """Main function to run the example task"""
    print("🤖 Starting Web Robot Automation...")
    
    task = ExampleTask()
    result = await task.execute_example_task()
    
    if result.success:
        print(f"✅ {result.message}")
        if result.data:
            print(f"📊 Data: {result.data}")
    else:
        print(f"❌ {result.message}")
        if result.error:
            print(f"🔍 Error: {result.error}")

if __name__ == "__main__":
    asyncio.run(main())
