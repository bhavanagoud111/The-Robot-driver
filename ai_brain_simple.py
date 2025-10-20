"""
AI Brain with MCP Integration - Simple Working Version
This demonstrates the AI-driven automation architecture with dynamic task execution.
"""

import json
import logging
import asyncio
from typing import Dict, Any, List, Optional
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class AutomationResult:
    """Result of an automation task"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class MCPPageAnalyzer:
    """
    Model Context Protocol (MCP) - Like page analyzer
    This provides detailed, structured information about the current webpage state
    """
    
    def __init__(self, page: Page):
        self.page = page
    
    async def analyze_page_context(self) -> Dict[str, Any]:
        """
        Analyze current page context using MCP-like approach
        Provides detailed, structured information about webpage state
        """
        try:
            print("🔍 Analyzing page context with MCP...")
            
            # Get basic page information
            page_info = {
                "url": self.page.url,
                "title": await self.page.title(),
                "viewport": await self.page.viewport_size(),
                "elements": []
            }
            
            # Get all interactive elements (MCP-like analysis)
            elements = await self.page.query_selector_all('input, button, a, select, textarea')
            
            print(f"📊 Found {len(elements)} interactive elements")
            
            for element in elements:
                try:
                    # Get element properties (MCP-like data)
                    element_data = await self.page.evaluate('''(el) => {
                        return {
                            tagName: el.tagName,
                            type: el.type || null,
                            id: el.id || null,
                            className: el.className || null,
                            placeholder: el.placeholder || null,
                            textContent: el.textContent?.trim() || null,
                            value: el.value || null,
                            role: el.getAttribute('role') || null,
                            ariaLabel: el.getAttribute('aria-label') || null,
                            href: el.href || null,
                            disabled: el.disabled || false,
                            visible: el.offsetParent !== null
                        }
                    }''', element)
                    
                    # Add element to analysis
                    page_info["elements"].append(element_data)
                    
                except Exception as e:
                    logger.warning(f"Failed to analyze element: {e}")
                    continue
            
            print(f"✅ Page analysis complete: {len(page_info['elements'])} elements")
            return page_info
            
        except Exception as e:
            logger.error(f"Failed to analyze page context: {e}")
            return {"error": str(e)}

class AIBrain:
    """
    AI-powered automation brain (Demo version with rule-based planning)
    """
    
    def __init__(self):
        pass
    
    async def generate_automation_plan(self, user_goal: str, page_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate automation plan based on user goal and page context
        (Demo version with rule-based planning)
        """
        try:
            print(f"🧠 Generating AI plan for: {user_goal}")
            
            # Analyze user goal to determine actions
            goal_lower = user_goal.lower()
            
            if "book" in goal_lower and "click" in goal_lower:
                plan = {
                    "plan": [
                        {
                            "step": 1,
                            "action": "click",
                            "selector": "h3 a",
                            "description": "Click on the first book product",
                            "timeout": 10000
                        }
                    ],
                    "expected_outcome": "Navigate to product page",
                    "confidence": 0.9
                }
            elif "title" in goal_lower or "price" in goal_lower:
                plan = {
                    "plan": [
                        {
                            "step": 1,
                            "action": "click",
                            "selector": "h3 a",
                            "description": "Click on the first book product",
                            "timeout": 10000
                        },
                        {
                            "step": 2,
                            "action": "wait",
                            "selector": "h1",
                            "description": "Wait for product page to load",
                            "timeout": 10000
                        },
                        {
                            "step": 3,
                            "action": "get_text",
                            "selector": "h1",
                            "description": "Get product title",
                            "timeout": 10000
                        },
                        {
                            "step": 4,
                            "action": "get_text",
                            "selector": ".price_color",
                            "description": "Get product price",
                            "timeout": 10000
                        }
                    ],
                    "expected_outcome": "Extract product title and price",
                    "confidence": 0.85
                }
            else:
                # Default plan
                plan = {
                    "plan": [
                        {
                            "step": 1,
                            "action": "get_text",
                            "selector": "h1",
                            "description": "Get page title",
                            "timeout": 10000
                        }
                    ],
                    "expected_outcome": "Get page information",
                    "confidence": 0.7
                }
            
            print(f"✅ AI plan generated: {len(plan['plan'])} steps")
            return plan
            
        except Exception as e:
            logger.error(f"Failed to generate automation plan: {e}")
            return {"error": str(e)}

class AIWebRobot:
    """
    AI-powered web robot that executes dynamic plans
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
        """Start the browser"""
        try:
            print("🤖 Starting AI Web Robot...")
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
            self.page = await self.context.new_page()
            print("✅ AI Web Robot started successfully")
        except Exception as e:
            print(f"❌ Failed to start AI Web Robot: {e}")
            raise
    
    async def close(self):
        """Close the browser"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            print("✅ AI Web Robot closed successfully")
        except Exception as e:
            print(f"❌ Error closing AI Web Robot: {e}")
    
    async def execute_action(self, action: str, selector: str = "", value: str = "", timeout: int = 10000) -> AutomationResult:
        """Execute a single action"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            if action == "navigate":
                print(f"🌐 Navigating to: {selector}")
                await self.page.goto(selector, timeout=timeout)
                await self.page.wait_for_load_state('networkidle', timeout=timeout)
                return AutomationResult(success=True, message=f"Navigated to {selector}")
            
            elif action == "click":
                print(f"🖱️  Clicking: {selector}")
                await self.page.wait_for_selector(selector, timeout=timeout)
                await self.page.click(selector)
                return AutomationResult(success=True, message=f"Clicked {selector}")
            
            elif action == "type":
                print(f"⌨️  Typing '{value}' into: {selector}")
                await self.page.wait_for_selector(selector, timeout=timeout)
                await self.page.fill(selector, value)
                return AutomationResult(success=True, message=f"Typed '{value}' into {selector}")
            
            elif action == "wait":
                print(f"⏳ Waiting for: {selector}")
                await self.page.wait_for_selector(selector, timeout=timeout)
                return AutomationResult(success=True, message=f"Waited for {selector}")
            
            elif action == "get_text":
                print(f"📖 Getting text from: {selector}")
                await self.page.wait_for_selector(selector, timeout=timeout)
                text = await self.page.text_content(selector)
                print(f"✅ Retrieved: {text}")
                return AutomationResult(success=True, message=f"Retrieved text from {selector}", data={"text": text})
            
            elif action == "scroll":
                print("📜 Scrolling page...")
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                return AutomationResult(success=True, message="Scrolled page")
            
            else:
                return AutomationResult(success=False, message=f"Unknown action: {action}")
                
        except Exception as e:
            print(f"❌ Action execution failed: {e}")
            return AutomationResult(success=False, message=f"Action failed: {action}", error=str(e))
    
    async def execute_ai_plan(self, plan: Dict[str, Any]) -> AutomationResult:
        """Execute the AI-generated automation plan"""
        try:
            if "error" in plan:
                return AutomationResult(success=False, message="AI plan generation failed", error=plan["error"])
            
            steps = plan.get("plan", [])
            if not steps:
                return AutomationResult(success=False, message="No steps in AI plan", error="Empty plan")
            
            print(f"\n🎯 Executing AI plan with {len(steps)} steps...")
            results = []
            
            for step in steps:
                step_num = step.get("step", 0)
                action = step.get("action", "")
                selector = step.get("selector", "")
                value = step.get("value", "")
                timeout = step.get("timeout", 10000)
                description = step.get("description", "")
                
                print(f"\n📋 Step {step_num}: {description}")
                print(f"   Action: {action}, Selector: {selector}")
                
                result = await self.execute_action(action, selector, value, timeout)
                results.append({
                    "step": step_num,
                    "action": action,
                    "success": result.success,
                    "message": result.message,
                    "data": result.data
                })
                
                if not result.success:
                    print(f"❌ Step {step_num} failed: {result.message}")
                    break
                else:
                    print(f"✅ Step {step_num} completed: {result.message}")
                
                # Small delay between steps
                await asyncio.sleep(1)
            
            # Determine overall success
            all_successful = all(step.get("success", False) for step in results)
            
            return AutomationResult(
                success=all_successful,
                message=f"AI plan execution {'completed successfully' if all_successful else 'failed'}",
                data={
                    "steps": results,
                    "expected_outcome": plan.get("expected_outcome", ""),
                    "confidence": plan.get("confidence", 0.0),
                    "total_steps": len(steps),
                    "successful_steps": sum(1 for step in results if step.get("success", False))
                }
            )
            
        except Exception as e:
            print(f"❌ AI plan execution failed: {e}")
            return AutomationResult(success=False, message="AI plan execution failed", error=str(e))

class AIBrainMCP:
    """
    Complete AI Brain with MCP integration (Simple working version)
    """
    
    def __init__(self):
        self.ai_brain = AIBrain()
        self.robot = AIWebRobot(headless=False)
    
    async def execute_ai_task(self, user_goal: str, page_url: str) -> AutomationResult:
        """
        Complete AI-driven task execution with MCP integration
        """
        try:
            print(f"\n🧠 Starting AI task: {user_goal}")
            print(f"🌐 Target URL: {page_url}")
            
            async with self.robot as robot:
                # Step 1: Navigate to page
                print("\n" + "="*60)
                print("STEP 1: Navigating to page")
                print("="*60)
                nav_result = await robot.execute_action("navigate", page_url)
                if not nav_result.success:
                    return AutomationResult(success=False, message="Failed to navigate to page", error=nav_result.error)
                
                # Step 2: Analyze page context using MCP
                print("\n" + "="*60)
                print("STEP 2: Analyzing page context with MCP")
                print("="*60)
                analyzer = MCPPageAnalyzer(robot.page)
                page_context = await analyzer.analyze_page_context()
                
                if "error" in page_context:
                    return AutomationResult(success=False, message="Failed to analyze page context", error=page_context["error"])
                
                # Step 3: Generate AI plan
                print("\n" + "="*60)
                print("STEP 3: Generating AI automation plan")
                print("="*60)
                plan = await self.ai_brain.generate_automation_plan(user_goal, page_context)
                
                if "error" in plan:
                    return AutomationResult(success=False, message="Failed to generate AI plan", error=plan["error"])
                
                # Step 4: Execute AI plan
                print("\n" + "="*60)
                print("STEP 4: Executing AI-generated plan")
                print("="*60)
                result = await robot.execute_ai_plan(plan)
                
                return result
                
        except Exception as e:
            print(f"❌ AI task execution failed: {e}")
            return AutomationResult(success=False, message="AI task execution failed", error=str(e))

async def main():
    """
    Main function to demonstrate AI Brain with MCP integration
    """
    print("🧠 AI Brain with MCP Integration - Simple Working Version")
    print("=" * 60)
    print("Advanced AI-driven automation with dynamic task execution")
    print("=" * 60)
    
    # Create AI Brain with MCP
    ai_brain = AIBrainMCP()
    
    # Example user goals
    user_goals = [
        "Find and click on the first book product",
        "Get the title and price of the first book"
    ]
    
    page_url = "https://books.toscrape.com/"
    
    for i, goal in enumerate(user_goals, 1):
        print(f"\n{'='*60}")
        print(f"AI TASK {i}: {goal}")
        print(f"{'='*60}")
        
        result = await ai_brain.execute_ai_task(goal, page_url)
        
        print(f"\n{'='*60}")
        print("📊 TASK RESULTS")
        print("=" * 60)
        
        if result.success:
            print(f"✅ {result.message}")
            if result.data:
                print(f"📊 Steps completed: {result.data.get('successful_steps', 0)}/{result.data.get('total_steps', 0)}")
                print(f"🎯 Expected outcome: {result.data.get('expected_outcome', 'N/A')}")
                print(f"🎲 Confidence: {result.data.get('confidence', 0.0):.2f}")
                
                # Show extracted data
                for step in result.data.get('steps', []):
                    if step.get('data', {}).get('text'):
                        print(f"📝 Extracted: {step['data']['text']}")
        else:
            print(f"❌ {result.message}")
            if result.error:
                print(f"🔍 Error: {result.error}")
        
        print(f"\n{'='*60}")
    
    print("\n🎉 AI Brain with MCP integration completed!")
    print("💡 This demonstrates the AI agent architecture with dynamic task execution")
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
