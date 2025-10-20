"""
AI Brain with MCP Integration - Advanced AI-driven automation
This module provides AI-powered task execution using OpenAI and MCP.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
from core_robot import WebRobot, AutomationResult
from database import get_db, AutomationTask, AutomationSession
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIBrain:
    """AI-powered automation brain using OpenAI and MCP"""
    
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.robot = WebRobot(headless=False)
    
    async def analyze_page_context(self, page_url: str) -> Dict[str, Any]:
        """Analyze current page context using MCP-like approach"""
        try:
            async with self.robot as robot:
                # Navigate to page
                nav_result = await robot.navigate_to(page_url)
                if not nav_result.success:
                    return {"error": "Failed to navigate to page"}
                
                # Get page information
                page_info = {
                    "url": page_url,
                    "title": await robot.page.title(),
                    "elements": []
                }
                
                # Get interactive elements (simplified MCP-like approach)
                elements = await robot.page.query_selector_all('input, button, a, select, textarea')
                for element in elements:
                    try:
                        tag_name = await element.evaluate('el => el.tagName')
                        element_type = await element.evaluate('el => el.type') if tag_name.lower() == 'input' else None
                        placeholder = await element.evaluate('el => el.placeholder') or ""
                        text = await element.evaluate('el => el.textContent') or ""
                        element_id = await element.evaluate('el => el.id') or ""
                        classes = await element.evaluate('el => el.className') or ""
                        
                        page_info["elements"].append({
                            "tag": tag_name.lower(),
                            "type": element_type,
                            "placeholder": placeholder,
                            "text": text.strip(),
                            "id": element_id,
                            "classes": classes
                        })
                    except Exception as e:
                        logger.warning(f"Failed to analyze element: {e}")
                        continue
                
                return page_info
                
        except Exception as e:
            logger.error(f"Failed to analyze page context: {e}")
            return {"error": str(e)}
    
    async def generate_automation_plan(self, user_goal: str, page_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate automation plan using AI"""
        try:
            # Prepare context for AI
            context_prompt = f"""
You are an expert web automation assistant. Given a user goal and page context, generate a step-by-step automation plan.

User Goal: {user_goal}

Page Context:
- URL: {page_context.get('url', 'Unknown')}
- Title: {page_context.get('title', 'Unknown')}
- Available Elements: {json.dumps(page_context.get('elements', []), indent=2)}

Generate a JSON response with the following structure:
{{
    "plan": [
        {{
            "step": 1,
            "action": "navigate|click|type|wait|get_text",
            "selector": "CSS selector or XPath",
            "value": "text to type (if action is 'type')",
            "description": "What this step does"
        }}
    ],
    "expected_outcome": "What should happen after all steps"
}}

Available actions:
- navigate: Go to a URL
- click: Click an element
- type: Type text into an input field
- wait: Wait for an element to appear
- get_text: Extract text from an element

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
    
    async def execute_ai_plan(self, plan: Dict[str, Any], task_id: int) -> AutomationResult:
        """Execute the AI-generated automation plan"""
        try:
            if "error" in plan:
                return AutomationResult(
                    success=False,
                    message="AI plan generation failed",
                    error=plan["error"]
                )
            
            steps = plan.get("plan", [])
            if not steps:
                return AutomationResult(
                    success=False,
                    message="No steps in AI plan",
                    error="Empty plan"
                )
            
            results = []
            
            async with self.robot as robot:
                for step in steps:
                    step_num = step.get("step", 0)
                    action = step.get("action", "")
                    selector = step.get("selector", "")
                    value = step.get("value", "")
                    description = step.get("description", "")
                    
                    logger.info(f"Executing step {step_num}: {description}")
                    
                    try:
                        if action == "navigate":
                            result = await robot.navigate_to(selector)
                        elif action == "click":
                            result = await robot.click_element(selector)
                        elif action == "type":
                            result = await robot.type_text(selector, value)
                        elif action == "wait":
                            result = await robot.wait_for_element(selector)
                        elif action == "get_text":
                            result = await robot.get_text(selector)
                        else:
                            result = AutomationResult(
                                success=False,
                                message=f"Unknown action: {action}",
                                error=f"Action '{action}' not supported"
                            )
                        
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
                            
                    except Exception as e:
                        logger.error(f"Step {step_num} execution failed: {e}")
                        results.append({
                            "step": step_num,
                            "action": action,
                            "success": False,
                            "message": f"Step execution failed: {e}",
                            "error": str(e)
                        })
                        break
            
            # Determine overall success
            all_successful = all(step.get("success", False) for step in results)
            
            return AutomationResult(
                success=all_successful,
                message=f"AI plan execution {'completed successfully' if all_successful else 'failed'}",
                data={
                    "steps": results,
                    "expected_outcome": plan.get("expected_outcome", ""),
                    "total_steps": len(steps),
                    "successful_steps": sum(1 for step in results if step.get("success", False))
                }
            )
            
        except Exception as e:
            logger.error(f"AI plan execution failed: {e}")
            return AutomationResult(
                success=False,
                message="AI plan execution failed",
                error=str(e)
            )
    
    async def execute_ai_task(self, user_goal: str, page_url: str) -> AutomationResult:
        """Complete AI-driven task execution"""
        try:
            # Analyze page context
            logger.info("Analyzing page context...")
            page_context = await self.analyze_page_context(page_url)
            
            if "error" in page_context:
                return AutomationResult(
                    success=False,
                    message="Failed to analyze page context",
                    error=page_context["error"]
                )
            
            # Generate automation plan
            logger.info("Generating automation plan...")
            plan = await self.generate_automation_plan(user_goal, page_context)
            
            if "error" in plan:
                return AutomationResult(
                    success=False,
                    message="Failed to generate automation plan",
                    error=plan["error"]
                )
            
            # Execute the plan
            logger.info("Executing AI-generated plan...")
            result = await self.execute_ai_plan(plan, task_id=0)  # task_id will be set by API
            
            return result
            
        except Exception as e:
            logger.error(f"AI task execution failed: {e}")
            return AutomationResult(
                success=False,
                message="AI task execution failed",
                error=str(e)
            )

# Example usage
async def main():
    """Example of AI Brain usage"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
        return
    
    print("🧠 Starting AI Brain Automation...")
    
    ai_brain = AIBrain(api_key)
    
    # Example task
    user_goal = "Find and click on the 'Login' button"
    page_url = "https://demo.opencart.com/"
    
    result = await ai_brain.execute_ai_task(user_goal, page_url)
    
    if result.success:
        print(f"✅ {result.message}")
        if result.data:
            print(f"📊 Execution Data: {json.dumps(result.data, indent=2)}")
    else:
        print(f"❌ {result.message}")
        if result.error:
            print(f"🔍 Error: {result.error}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
