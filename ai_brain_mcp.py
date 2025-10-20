"""
AI Brain with MCP Integration - Advanced AI-driven automation
This module provides AI-powered task execution using OpenAI and MCP-like approach.
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
            # Get basic page information
            page_info = {
                "url": self.page.url,
                "title": await self.page.title(),
                "viewport": await self.page.viewport_size(),
                "elements": []
            }
            
            # Get all interactive elements (MCP-like analysis)
            elements = await self.page.query_selector_all('input, button, a, select, textarea, [role="button"], [onclick]')
            
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
                            visible: el.offsetParent !== null,
                            boundingBox: el.getBoundingClientRect()
                        }
                    }''', element)
                    
                    # Add element to analysis
                    page_info["elements"].append(element_data)
                    
                except Exception as e:
                    logger.warning(f"Failed to analyze element: {e}")
                    continue
            
            # Get page structure information
            page_info["structure"] = {
                "headings": await self._get_headings(),
                "forms": await self._get_forms(),
                "links": await self._get_links(),
                "images": await self._get_images()
            }
            
            return page_info
            
        except Exception as e:
            logger.error(f"Failed to analyze page context: {e}")
            return {"error": str(e)}
    
    async def _get_headings(self) -> List[Dict[str, Any]]:
        """Get page headings for structure analysis"""
        try:
            headings = await self.page.query_selector_all('h1, h2, h3, h4, h5, h6')
            return [
                {
                    "level": int(h.tag_name[1]),
                    "text": await h.text_content(),
                    "id": await h.get_attribute("id")
                }
                for h in headings
            ]
        except:
            return []
    
    async def _get_forms(self) -> List[Dict[str, Any]]:
        """Get form information"""
        try:
            forms = await self.page.query_selector_all('form')
            form_data = []
            for form in forms:
                inputs = await form.query_selector_all('input, select, textarea')
                form_data.append({
                    "action": await form.get_attribute("action"),
                    "method": await form.get_attribute("method"),
                    "inputs": [
                        {
                            "type": await inp.get_attribute("type"),
                            "name": await inp.get_attribute("name"),
                            "placeholder": await inp.get_attribute("placeholder")
                        }
                        for inp in inputs
                    ]
                })
            return form_data
        except:
            return []
    
    async def _get_links(self) -> List[Dict[str, Any]]:
        """Get link information"""
        try:
            links = await self.page.query_selector_all('a[href]')
            return [
                {
                    "text": await link.text_content(),
                    "href": await link.get_attribute("href"),
                    "title": await link.get_attribute("title")
                }
                for link in links[:10]  # Limit to first 10 links
            ]
        except:
            return []
    
    async def _get_images(self) -> List[Dict[str, Any]]:
        """Get image information"""
        try:
            images = await self.page.query_selector_all('img')
            return [
                {
                    "src": await img.get_attribute("src"),
                    "alt": await img.get_attribute("alt"),
                    "title": await img.get_attribute("title")
                }
                for img in images[:5]  # Limit to first 5 images
            ]
        except:
            return []

class AIBrain:
    """
    AI-powered automation brain using OpenAI and MCP-like approach
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = None
        self._init_openai_client()
    
    def _init_openai_client(self):
        """Initialize OpenAI client"""
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=self.api_key)
        except ImportError:
            logger.error("OpenAI library not installed. Please install: pip install openai")
            raise
    
    async def generate_automation_plan(self, user_goal: str, page_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate automation plan using AI based on user goal and page context
        """
        try:
            # Prepare context for AI
            context_prompt = f"""
You are an expert web automation assistant. Given a user goal and detailed page context, generate a step-by-step automation plan.

User Goal: {user_goal}

Page Context:
- URL: {page_context.get('url', 'Unknown')}
- Title: {page_context.get('title', 'Unknown')}
- Viewport: {page_context.get('viewport', {})}
- Available Elements: {json.dumps(page_context.get('elements', []), indent=2)}
- Page Structure: {json.dumps(page_context.get('structure', {}), indent=2)}

Generate a JSON response with the following structure:
{{
    "plan": [
        {{
            "step": 1,
            "action": "navigate|click|type|wait|get_text|scroll",
            "selector": "CSS selector or XPath",
            "value": "text to type (if action is 'type')",
            "description": "What this step does",
            "timeout": 10000
        }}
    ],
    "expected_outcome": "What should happen after all steps",
    "confidence": 0.95
}}

Available actions:
- navigate: Go to a URL
- click: Click an element
- type: Type text into an input field
- wait: Wait for an element to appear
- get_text: Extract text from an element
- scroll: Scroll the page

Return only valid JSON.
"""
            
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert web automation assistant. Always respond with valid JSON."},
                    {"role": "user", "content": context_prompt}
                ],
                temperature=0.1
            )
            
            plan_text = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                plan = json.loads(plan_text)
                return plan
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse AI response as JSON: {e}")
                return {"error": "Invalid JSON response from AI"}
                
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
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1280, 'height': 720}
            )
            self.page = await self.context.new_page()
            logger.info("AI Web Robot started successfully")
        except Exception as e:
            logger.error(f"Failed to start AI Web Robot: {e}")
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
            logger.info("AI Web Robot closed successfully")
        except Exception as e:
            logger.error(f"Error closing AI Web Robot: {e}")
    
    async def execute_action(self, action: str, selector: str = "", value: str = "", timeout: int = 10000) -> AutomationResult:
        """Execute a single action"""
        try:
            if not self.page:
                raise Exception("Browser not started")
            
            if action == "navigate":
                await self.page.goto(selector, timeout=timeout)
                await self.page.wait_for_load_state('networkidle', timeout=timeout)
                return AutomationResult(success=True, message=f"Navigated to {selector}")
            
            elif action == "click":
                await self.page.wait_for_selector(selector, timeout=timeout)
                await self.page.click(selector)
                return AutomationResult(success=True, message=f"Clicked {selector}")
            
            elif action == "type":
                await self.page.wait_for_selector(selector, timeout=timeout)
                await self.page.fill(selector, value)
                return AutomationResult(success=True, message=f"Typed '{value}' into {selector}")
            
            elif action == "wait":
                await self.page.wait_for_selector(selector, timeout=timeout)
                return AutomationResult(success=True, message=f"Waited for {selector}")
            
            elif action == "get_text":
                await self.page.wait_for_selector(selector, timeout=timeout)
                text = await self.page.text_content(selector)
                return AutomationResult(success=True, message=f"Retrieved text from {selector}", data={"text": text})
            
            elif action == "scroll":
                await self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                return AutomationResult(success=True, message="Scrolled page")
            
            else:
                return AutomationResult(success=False, message=f"Unknown action: {action}")
                
        except Exception as e:
            logger.error(f"Action execution failed: {e}")
            return AutomationResult(success=False, message=f"Action failed: {action}", error=str(e))
    
    async def execute_ai_plan(self, plan: Dict[str, Any]) -> AutomationResult:
        """Execute the AI-generated automation plan"""
        try:
            if "error" in plan:
                return AutomationResult(success=False, message="AI plan generation failed", error=plan["error"])
            
            steps = plan.get("plan", [])
            if not steps:
                return AutomationResult(success=False, message="No steps in AI plan", error="Empty plan")
            
            results = []
            
            for step in steps:
                step_num = step.get("step", 0)
                action = step.get("action", "")
                selector = step.get("selector", "")
                value = step.get("value", "")
                timeout = step.get("timeout", 10000)
                description = step.get("description", "")
                
                logger.info(f"Executing step {step_num}: {description}")
                
                result = await self.execute_action(action, selector, value, timeout)
                results.append({
                    "step": step_num,
                    "action": action,
                    "success": result.success,
                    "message": result.message,
                    "data": result.data
                })
                
                if not result.success:
                    logger.error(f"Step {step_num} failed: {result.message}")
                    break
                
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
            logger.error(f"AI plan execution failed: {e}")
            return AutomationResult(success=False, message="AI plan execution failed", error=str(e))

class AIBrainMCP:
    """
    Complete AI Brain with MCP integration
    """
    
    def __init__(self, api_key: str):
        self.ai_brain = AIBrain(api_key)
        self.robot = AIWebRobot(headless=False)
    
    async def execute_ai_task(self, user_goal: str, page_url: str) -> AutomationResult:
        """
        Complete AI-driven task execution with MCP integration
        """
        try:
            logger.info(f"Starting AI task: {user_goal}")
            
            async with self.robot as robot:
                # Step 1: Navigate to page
                nav_result = await robot.execute_action("navigate", page_url)
                if not nav_result.success:
                    return AutomationResult(success=False, message="Failed to navigate to page", error=nav_result.error)
                
                # Step 2: Analyze page context using MCP
                logger.info("Analyzing page context with MCP...")
                analyzer = MCPPageAnalyzer(robot.page)
                page_context = await analyzer.analyze_page_context()
                
                if "error" in page_context:
                    return AutomationResult(success=False, message="Failed to analyze page context", error=page_context["error"])
                
                # Step 3: Generate AI plan
                logger.info("Generating AI automation plan...")
                plan = await self.ai_brain.generate_automation_plan(user_goal, page_context)
                
                if "error" in plan:
                    return AutomationResult(success=False, message="Failed to generate AI plan", error=plan["error"])
                
                # Step 4: Execute AI plan
                logger.info("Executing AI-generated plan...")
                result = await robot.execute_ai_plan(plan)
                
                return result
                
        except Exception as e:
            logger.error(f"AI task execution failed: {e}")
            return AutomationResult(success=False, message="AI task execution failed", error=str(e))

async def main():
    """
    Main function to demonstrate AI Brain with MCP integration
    """
    print("🧠 AI Brain with MCP Integration")
    print("=" * 60)
    print("Advanced AI-driven automation with dynamic task execution")
    print("=" * 60)
    
    # Check for OpenAI API key
    import os
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API key not found!")
        print("Please set OPENAI_API_KEY environment variable")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        return 1
    
    # Create AI Brain with MCP
    ai_brain = AIBrainMCP(api_key)
    
    # Example user goals
    user_goals = [
        "Find and click on the first book product",
        "Get the title and price of the first book",
        "Navigate to the product page and extract product information"
    ]
    
    page_url = "https://books.toscrape.com/"
    
    for i, goal in enumerate(user_goals, 1):
        print(f"\n{'='*60}")
        print(f"AI TASK {i}: {goal}")
        print(f"{'='*60}")
        
        result = await ai_brain.execute_ai_task(goal, page_url)
        
        if result.success:
            print(f"✅ {result.message}")
            if result.data:
                print(f"📊 Steps completed: {result.data.get('successful_steps', 0)}/{result.data.get('total_steps', 0)}")
                print(f"🎯 Expected outcome: {result.data.get('expected_outcome', 'N/A')}")
                print(f"🎲 Confidence: {result.data.get('confidence', 0.0):.2f}")
        else:
            print(f"❌ {result.message}")
            if result.error:
                print(f"🔍 Error: {result.error}")
        
        print(f"\n{'='*60}")
    
    print("\n🎉 AI Brain with MCP integration completed!")
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
