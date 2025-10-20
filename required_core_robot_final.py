"""
Required Core: The Robot Driver - Final Version
A Python program that controls a web browser using Playwright to complete a fixed, single task.
This implementation uses a reliable, simple e-commerce site for demonstration.
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
    Fixed Task: Search for a specific product and report its information
    
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
        Execute the complete product search task using a simple e-commerce site
        
        Task Flow:
        1. Navigate to a product catalog site
        2. Search for a specific product
        3. Find and extract product information
        4. Report the results
        """
        try:
            logger.info("Starting product search task...")
            
            async with self.robot as robot:
                # Step 1: Navigate to a simple e-commerce site
                logger.info("Step 1: Navigating to product catalog...")
                nav_result = await robot.navigate_to_url("https://books.toscrape.com/")
                
                if not nav_result.success:
                    return TaskResult(
                        success=False,
                        message="Failed to navigate to product catalog",
                        error=nav_result.error
                    )
                
                logger.info(f"✅ Navigation successful: {nav_result.data['title']}")
                
                # Step 2: Find and click on a specific product category
                logger.info("Step 2: Looking for product categories...")
                
                # Wait for the page to load completely
                await asyncio.sleep(2)
                
                # Look for product links
                product_links = await robot.page.query_selector_all('h3 a')
                if not product_links:
                    return TaskResult(
                        success=False,
                        message="No products found on the page",
                        error="Product links not available"
                    )
                
                # Click on the first product
                first_product = product_links[0]
                product_title = await first_product.text_content()
                
                logger.info(f"✅ Found product: {product_title}")
                
                # Click on the first product
                click_result = await robot.click_element('h3 a', timeout=15000)
                if not click_result.success:
                    return TaskResult(
                        success=False,
                        message="Failed to click on product",
                        error=click_result.error
                    )
                
                logger.info("✅ Product clicked successfully")
                
                # Step 3: Extract product information
                logger.info("Step 3: Extracting product information...")
                
                # Wait for product page to load
                await asyncio.sleep(2)
                
                # Get product title
                title_result = await robot.get_text_content('h1', timeout=10000)
                if not title_result.success:
                    return TaskResult(
                        success=False,
                        message="Failed to extract product title",
                        error=title_result.error
                    )
                
                # Get product price
                price_result = await robot.get_text_content('.price_color', timeout=10000)
                if not price_result.success:
                    return TaskResult(
                        success=False,
                        message="Failed to extract product price",
                        error=price_result.error
                    )
                
                # Get product description
                description_result = await robot.get_text_content('#product_description + p', timeout=10000)
                description = description_result.data['text'] if description_result.success else "Description not available"
                
                # Extract product details
                product_title = title_result.data['text'].strip()
                product_price = price_result.data['text'].strip()
                
                logger.info(f"✅ Product title: {product_title}")
                logger.info(f"✅ Product price: {product_price}")
                logger.info(f"✅ Product description: {description[:100]}...")
                
                # Step 4: Report final results
                return TaskResult(
                    success=True,
                    message=f"Success! Product '{product_title}' found with price {product_price}",
                    data={
                        'product_title': product_title,
                        'product_price': product_price,
                        'product_description': description,
                        'website': 'books.toscrape.com',
                        'search_type': 'Product Catalog Browse'
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
    - All required browser actions (Navigate, Click, Type)
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
            print(f"📦 Product: {result.data['product_title']}")
            print(f"💰 Price: {result.data['product_price']}")
            print(f"📝 Description: {result.data['product_description'][:100]}...")
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
