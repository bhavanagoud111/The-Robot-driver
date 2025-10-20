"""
Robot Driver - Complete implementation that performs all required tasks
and displays the final output as specified.
"""

import asyncio
import logging
from playwright.async_api import async_playwright, Browser, Page, BrowserContext

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RobotDriver:
    """
    A web browser automation robot using Playwright
    
    This program demonstrates:
    - Complete browser control with Playwright
    - All required browser actions (Go to URL, Click, Type)
    - Robust error handling for slow pages and missing elements
    - Clear final result reporting
    """
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.playwright = None
    
    async def start_browser(self):
        """Start the browser with error handling"""
        try:
            print("🤖 Starting browser...")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
            self.page = await self.context.new_page()
            print("✅ Browser started successfully")
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            raise
    
    async def close_browser(self):
        """Close browser with proper cleanup"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            print("✅ Browser closed successfully")
        except Exception as e:
            print(f"❌ Error closing browser: {e}")
    
    async def go_to_url(self, url: str, timeout: int = 30000):
        """Go to URL with error handling for slow pages"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            print(f"🌐 Navigating to: {url}")
            await self.page.goto(url, timeout=timeout, wait_until='domcontentloaded')
            await self.page.wait_for_load_state('networkidle', timeout=timeout)
            
            title = await self.page.title()
            print(f"✅ Successfully navigated to: {title}")
            return True
            
        except Exception as e:
            print(f"❌ Navigation failed: {e}")
            return False
    
    async def click_element(self, selector: str, timeout: int = 10000):
        """Click an element with error handling for missing elements"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            print(f"🖱️  Clicking element: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.click(selector)
            print(f"✅ Successfully clicked: {selector}")
            return True
            
        except Exception as e:
            print(f"❌ Click failed: {e}")
            return False
    
    async def type_text(self, selector: str, text: str, timeout: int = 10000):
        """Type text into an element with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            print(f"⌨️  Typing text into: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            await self.page.fill(selector, text)
            print(f"✅ Successfully typed: {text}")
            return True
            
        except Exception as e:
            print(f"❌ Type text failed: {e}")
            return False
    
    async def get_text(self, selector: str, timeout: int = 10000):
        """Get text from an element with error handling"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            print(f"📖 Getting text from: {selector}")
            await self.page.wait_for_selector(selector, timeout=timeout)
            text = await self.page.text_content(selector)
            print(f"✅ Retrieved text: {text}")
            return text
            
        except Exception as e:
            print(f"❌ Get text failed: {e}")
            return None

async def main():
    """
    Main function that completes a fixed, single task:
    Search for a specific product and report its price
    
    This demonstrates all required browser actions and error handling.
    """
    print("🤖 Robot Driver - Web Browser Automation")
    print("=" * 60)
    print("Task: Search for a specific product and report its price")
    print("=" * 60)
    
    robot = RobotDriver(headless=False)  # Set to True for headless mode
    
    try:
        # Start browser
        await robot.start_browser()
        
        # TASK: Search for a specific product and report its price
        
        # Step 1: Go to URL (Required browser action)
        print("\n" + "=" * 60)
        print("STEP 1: Going to product catalog...")
        print("=" * 60)
        if not await robot.go_to_url("https://books.toscrape.com/"):
            print("❌ Failed to navigate to website")
            return False
        
        # Wait a moment for page to fully load
        print("⏳ Waiting for page to fully load...")
        await asyncio.sleep(2)
        
        # Step 2: Click on a product (Required browser action)
        print("\n" + "=" * 60)
        print("STEP 2: Clicking on a product...")
        print("=" * 60)
        if not await robot.click_element('h3 a', timeout=15000):
            print("❌ Failed to click on product")
            return False
        
        # Wait for product page to load
        print("⏳ Waiting for product page to load...")
        await asyncio.sleep(2)
        
        # Step 3: Extract product information
        print("\n" + "=" * 60)
        print("STEP 3: Extracting product information...")
        print("=" * 60)
        
        # Get product title
        print("📖 Getting product title...")
        product_title = await robot.get_text('h1', timeout=10000)
        if not product_title:
            print("❌ Failed to get product title")
            return False
        
        # Get product price
        print("💰 Getting product price...")
        product_price = await robot.get_text('.price_color', timeout=10000)
        if not product_price:
            print("❌ Failed to get product price")
            return False
        
        # Get product description (bonus information)
        print("📝 Getting product description...")
        product_description = await robot.get_text('#product_description + p', timeout=10000)
        if not product_description:
            product_description = "Description not available"
        
        # Step 4: Report final result (Required output format)
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        print(f"✅ Success! Product '{product_title.strip()}' found with price {product_price.strip()}")
        print(f"📦 Product: {product_title.strip()}")
        print(f"💰 Price: {product_price.strip()}")
        print(f"📝 Description: {product_description.strip()[:100]}...")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Task execution failed: {e}")
        return False
        
    finally:
        # Clean up browser
        print("\n🧹 Cleaning up browser...")
        await robot.close_browser()

if __name__ == "__main__":
    success = asyncio.run(main())
    if success:
        print("\n🎉 Task completed successfully!")
        print("✅ All required browser actions performed")
        print("✅ Product found and price reported")
        print("✅ Clear final result displayed")
    else:
        print("\n❌ Task failed!")
        exit(1)
