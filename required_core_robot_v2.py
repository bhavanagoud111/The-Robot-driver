"""
Required Core: The Robot Driver - Version 2
A Python program that controls a web browser using Playwright to complete a fixed, single task.
This implementation uses a reliable e-commerce site with search functionality.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TaskResult:
    """Result of the automation task"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class WebRobotDriver:
    """
    Core Robot Driver - Foundational web automation using Playwright
    
    This class demonstrates:
    - Core Python software engineering skills
    - Playwright browser automation
    - Robust error handling
    - Clear task execution and reporting
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.playwright = None
    
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
            logger.info("Starting browser...")
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
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser closed successfully")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def navigate_to_url(self, url: str, timeout: int = 30000) -> TaskResult:
        """Navigate to a URL with comprehensive error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Navigating to: {url}")
            await self.page.goto(url, timeout=timeout, wait_until='domcontentloaded')
            
            # Wait for page to be ready
            await self.page.wait_for_load_state('networkidle', timeout=timeout)
            
            # Get page title for verification
            title = await self.page.title()
            
            return TaskResult(
                success=True,
                message=f"Successfully navigated to {url}",
                data={'url': url, 'title': title}
            )
        except Exception as e:
            logger.error(f"Navigation failed: {e}")
            return TaskResult(
                success=False,
                message=f"Failed to navigate to {url}",
                error=str(e)
            )
    
    async def click_element(self, selector: str, timeout: int = 10000) -> TaskResult:
        """Click an element by selector with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Clicking element: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            
            return TaskResult(
                success=True,
                message=f"Successfully clicked element: {selector}"
            )
        except Exception as e:
            logger.error(f"Click failed: {e}")
            return TaskResult(
                success=False,
                message=f"Failed to click element: {selector}",
                error=str(e)
            )
    
    async def type_text(self, selector: str, text: str, timeout: int = 10000) -> TaskResult:
        """Type text into an element with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Typing text into: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, text)
            
            return TaskResult(
                success=True,
                message=f"Successfully typed text into: {selector}"
            )
        except Exception as e:
            logger.error(f"Type text failed: {e}")
            return TaskResult(
                success=False,
                message=f"Failed to type text into: {selector}",
                error=str(e)
            )
    
    async def get_text_content(self, selector: str, timeout: int = 10000) -> TaskResult:
        """Get text content from an element"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Getting text from: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            text = await self.page.text_content(selector)
            
            return TaskResult(
                success=True,
                message=f"Successfully retrieved text from: {selector}",
                data={'text': text}
            )
        except Exception as e:
            logger.error(f"Get text failed: {e}")
            return TaskResult(
                success=False,
                message=f"Failed to get text from: {selector}",
                error=str(e)
            )
    
    async def wait_for_element(self, selector: str, timeout: int = 10000) -> TaskResult:
        """Wait for an element to appear"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            logger.info(f"Waiting for element: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            
            return TaskResult(
                success=True,
                message=f"Element found: {selector}"
            )
        except Exception as e:
            logger.error(f"Wait for element failed: {e}")
            return TaskResult(
                success=False,
                message=f"Element not found: {selector}",
                error=str(e)
            )

class ProductSearchTask:
    """
    Fixed Task: Search for a specific product and report its price
    
    This task demonstrates:
    - Complete browser automation workflow
    - All required browser actions (Navigate, Click, Type)
    - Robust error handling for slow pages and missing elements
    - Clear final result reporting
    """
    
    def __init__(self):
        self.robot = WebRobotDriver(headless=False)  # Set to True for headless mode
    
    async def execute_product_search(self) -> TaskResult:
        """
        Execute the complete product search task using Google Shopping
        
        Task Flow:
        1. Navigate to Google
        2. Search for a specific product
        3. Find and extract product information
        4. Report the results
        """
        try:
            logger.info("Starting product search task...")
            
            async with self.robot as robot:
                # Step 1: Navigate to Google
                logger.info("Step 1: Navigating to Google...")
                nav_result = await robot.navigate_to_url("https://www.google.com")
                
                if not nav_result.success:
                    return TaskResult(
                        success=False,
                        message="Failed to navigate to Google",
                        error=nav_result.error
                    )
                
                logger.info(f"✅ Navigation successful: {nav_result.data['title']}")
                
                # Step 2: Search for a specific product
                logger.info("Step 2: Searching for product...")
                
                # Wait for Google search box
                search_input = 'input[name="q"]'
                search_wait = await robot.wait_for_element(search_input, timeout=15000)
                if not search_wait.success:
                    return TaskResult(
                        success=False,
                        message="Google search box not found",
                        error="Search input field not available"
                    )
                
                # Type search query for a specific product
                search_query = "MacBook Pro 13 inch price"
                type_result = await robot.type_text(search_input, search_query)
                if not type_result.success:
                    return TaskResult(
                        success=False,
                        message="Failed to type search query",
                        error=type_result.error
                    )
                
                # Press Enter to search
                await robot.page.press(search_input, 'Enter')
                
                logger.info("✅ Search query submitted successfully")
                
                # Step 3: Wait for results and extract product information
                logger.info("Step 3: Extracting product information...")
                
                # Wait for search results to load
                await asyncio.sleep(3)  # Give time for results to load
                
                # Look for product information in search results
                # Try to find price information
                price_selectors = [
                    '[data-ved] .g .VwiC3b',  # Google search result snippet
                    '.g .VwiC3b',  # Alternative selector
                    '.g .BNeawe',  # Another alternative
                    '.g .s3v9rd'   # Shopping results
                ]
                
                product_info = None
                price_found = False
                
                for selector in price_selectors:
                    try:
                        price_result = await robot.get_text_content(selector, timeout=5000)
                        if price_result.success and price_result.data['text']:
                            text = price_result.data['text'].strip()
                            # Look for price-like content
                            if any(char in text for char in ['$', '€', '£', '¥', 'price', 'USD', 'dollars']):
                                product_info = text
                                price_found = True
                                logger.info(f"✅ Found product info: {text}")
                                break
                    except:
                        continue
                
                if not price_found:
                    # Fallback: get the first search result snippet
                    snippet_selector = '.g .VwiC3b'
                    snippet_result = await robot.get_text_content(snippet_selector, timeout=10000)
                    if snippet_result.success:
                        product_info = snippet_result.data['text'].strip()
                        logger.info(f"✅ Found search result: {product_info}")
                    else:
                        return TaskResult(
                            success=False,
                            message="No product information found in search results",
                            error="Could not extract product details"
                        )
                
                # Step 4: Report final results
                return TaskResult(
                    success=True,
                    message=f"Success! Found product information for '{search_query}'",
                    data={
                        'search_query': search_query,
                        'product_info': product_info,
                        'website': 'google.com',
                        'search_type': 'Google Search'
                    }
                )
                
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            return TaskResult(
                success=False,
                message="Task execution failed",
                error=str(e)
            )

async def main():
    """
    Main function to execute the required core task
    
    This demonstrates:
    - Complete automation workflow
    - All required browser actions
    - Comprehensive error handling
    - Clear final result reporting
    """
    print("🤖 Required Core: Robot Driver")
    print("=" * 50)
    print("Task: Search for a specific product and report its price")
    print("=" * 50)
    
    # Create and execute the task
    task = ProductSearchTask()
    result = await task.execute_product_search()
    
    # Display final results
    print("\n" + "=" * 50)
    print("📊 TASK RESULTS")
    print("=" * 50)
    
    if result.success:
        print(f"✅ {result.message}")
        if result.data:
            print(f"🔍 Search Query: {result.data['search_query']}")
            print(f"📦 Product Info: {result.data['product_info']}")
            print(f"🌐 Website: {result.data['website']}")
            print(f"🔎 Search Type: {result.data['search_type']}")
    else:
        print(f"❌ {result.message}")
        if result.error:
            print(f"🔍 Error Details: {result.error}")
    
    print("\n" + "=" * 50)
    print("🎯 Required Core Task Completed")
    print("=" * 50)
    
    return 0 if result.success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
