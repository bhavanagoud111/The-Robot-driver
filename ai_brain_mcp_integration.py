#!/usr/bin/env python3
"""
AI Brain with MCP (Model Context Protocol) Integration
This implements the proper AI agent architecture as specified in the requirements.
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from playwright.async_api import async_playwright, Page, Browser
import openai
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class MCPPageContext:
    """MCP Page Context - structured information about the current page"""
    url: str
    title: str
    elements: List[Dict[str, Any]]
    accessibility_data: Dict[str, Any]
    page_structure: Dict[str, Any]
    interactive_elements: List[Dict[str, Any]]

@dataclass
class AIPlan:
    """AI-generated execution plan"""
    steps: List[Dict[str, Any]]
    confidence: float
    reasoning: str
    expected_outcome: str

class MCPAnalyzer:
    """MCP Server - analyzes page context and provides structured information"""
    
    def __init__(self):
        self.page = None
    
    async def analyze_page_context(self, page: Page) -> MCPPageContext:
        """Analyze page context using MCP principles"""
        try:
            logger.info("MCP: Analyzing page context...")
            
            # Get basic page information
            url = page.url
            title = await page.title()
            
            # Extract page elements with accessibility data
            elements = await self._extract_page_elements(page)
            
            # Get accessibility data
            accessibility_data = await self._get_accessibility_data(page)
            
            # Analyze page structure
            page_structure = await self._analyze_page_structure(page)
            
            # Find interactive elements
            interactive_elements = await self._find_interactive_elements(page)
            
            context = MCPPageContext(
                url=url,
                title=title,
                elements=elements,
                accessibility_data=accessibility_data,
                page_structure=page_structure,
                interactive_elements=interactive_elements
            )
            
            logger.info(f"MCP: Page context analyzed - {len(elements)} elements found")
            return context
            
        except Exception as e:
            logger.error(f"MCP: Error analyzing page context: {e}")
            raise
    
    async def _extract_page_elements(self, page: Page) -> List[Dict[str, Any]]:
        """Extract page elements with their properties"""
        elements = []
        
        try:
            # Get all interactive elements
            selectors = [
                'input', 'button', 'select', 'textarea', 'a', 'form',
                '[role="button"]', '[role="link"]', '[role="textbox"]',
                '[onclick]', '[data-testid]', '[aria-label]'
            ]
            
            for selector in selectors:
                try:
                    element_list = await page.query_selector_all(selector)
                    for element in element_list:
                        try:
                            element_info = await self._get_element_info(element, selector)
                            if element_info:
                                elements.append(element_info)
                        except:
                            continue
                except:
                    continue
            
            return elements
            
        except Exception as e:
            logger.error(f"MCP: Error extracting elements: {e}")
            return []
    
    async def _get_element_info(self, element, selector: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about an element"""
        try:
            # Get element properties
            tag_name = await element.evaluate('el => el.tagName')
            element_type = await element.evaluate('el => el.type')
            placeholder = await element.evaluate('el => el.placeholder')
            aria_label = await element.evaluate('el => el.getAttribute("aria-label")')
            role = await element.evaluate('el => el.getAttribute("role")')
            text_content = await element.evaluate('el => el.textContent')
            is_visible = await element.is_visible()
            is_enabled = await element.is_enabled()
            
            # Get position and size
            bounding_box = await element.bounding_box()
            
            return {
                'tag': tag_name.lower(),
                'type': element_type,
                'selector': selector,
                'placeholder': placeholder,
                'aria_label': aria_label,
                'role': role,
                'text': text_content.strip() if text_content else '',
                'visible': is_visible,
                'enabled': is_enabled,
                'position': bounding_box,
                'interactive': tag_name.lower() in ['input', 'button', 'select', 'textarea', 'a']
            }
            
        except Exception as e:
            logger.error(f"MCP: Error getting element info: {e}")
            return None
    
    async def _get_accessibility_data(self, page: Page) -> Dict[str, Any]:
        """Get accessibility data from the page"""
        try:
            # Get page accessibility information
            accessibility_data = {
                'headings': [],
                'landmarks': [],
                'forms': [],
                'links': []
            }
            
            # Get headings
            headings = await page.query_selector_all('h1, h2, h3, h4, h5, h6')
            for heading in headings:
                text = await heading.inner_text()
                level = await heading.evaluate('el => parseInt(el.tagName[1])')
                accessibility_data['headings'].append({'text': text, 'level': level})
            
            # Get landmarks
            landmarks = await page.query_selector_all('[role="main"], [role="navigation"], [role="banner"], [role="contentinfo"]')
            for landmark in landmarks:
                role = await landmark.evaluate('el => el.getAttribute("role")')
                text = await landmark.inner_text()
                accessibility_data['landmarks'].append({'role': role, 'text': text[:100]})
            
            return accessibility_data
            
        except Exception as e:
            logger.error(f"MCP: Error getting accessibility data: {e}")
            return {}
    
    async def _analyze_page_structure(self, page: Page) -> Dict[str, Any]:
        """Analyze the overall page structure"""
        try:
            structure = {
                'has_navigation': False,
                'has_search': False,
                'has_forms': False,
                'has_products': False,
                'page_type': 'unknown'
            }
            
            # Check for navigation
            nav_elements = await page.query_selector_all('nav, [role="navigation"]')
            structure['has_navigation'] = len(nav_elements) > 0
            
            # Check for search
            search_elements = await page.query_selector_all('input[type="search"], input[placeholder*="search" i]')
            structure['has_search'] = len(search_elements) > 0
            
            # Check for forms
            forms = await page.query_selector_all('form')
            structure['has_forms'] = len(forms) > 0
            
            # Check for products (e-commerce indicators)
            product_indicators = await page.query_selector_all('[data-testid*="product"], .product, [class*="product"]')
            structure['has_products'] = len(product_indicators) > 0
            
            # Determine page type
            if structure['has_products']:
                structure['page_type'] = 'ecommerce'
            elif structure['has_search']:
                structure['page_type'] = 'search'
            elif structure['has_forms']:
                structure['page_type'] = 'form'
            else:
                structure['page_type'] = 'content'
            
            return structure
            
        except Exception as e:
            logger.error(f"MCP: Error analyzing page structure: {e}")
            return {}
    
    async def _find_interactive_elements(self, page: Page) -> List[Dict[str, Any]]:
        """Find all interactive elements on the page"""
        interactive_elements = []
        
        try:
            # Find clickable elements
            clickable_selectors = [
                'button', 'a', 'input[type="submit"]', 'input[type="button"]',
                '[onclick]', '[role="button"]', '[data-testid*="button"]'
            ]
            
            for selector in clickable_selectors:
                elements = await page.query_selector_all(selector)
                for element in elements:
                    try:
                        text = await element.inner_text()
                        is_visible = await element.is_visible()
                        if is_visible and text.strip():
                            interactive_elements.append({
                                'type': 'clickable',
                                'selector': selector,
                                'text': text.strip(),
                                'action': 'click'
                            })
                    except:
                        continue
            
            # Find input elements
            input_elements = await page.query_selector_all('input, textarea, select')
            for element in input_elements:
                try:
                    element_type = await element.evaluate('el => el.type')
                    placeholder = await element.evaluate('el => el.placeholder')
                    is_visible = await element.is_visible()
                    if is_visible:
                        interactive_elements.append({
                            'type': 'input',
                            'element_type': element_type,
                            'placeholder': placeholder,
                            'action': 'type'
                        })
                except:
                    continue
            
            return interactive_elements
            
        except Exception as e:
            logger.error(f"MCP: Error finding interactive elements: {e}")
            return []

class LLMPlanner:
    """LLM-based plan generator using OpenAI"""
    
    def __init__(self, api_key: str = None):
        self.client = None
        if api_key:
            self.client = openai.OpenAI(api_key=api_key)
        else:
            # Try to get from environment
            import os
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_plan(self, user_goal: str, page_context: MCPPageContext) -> AIPlan:
        """Generate AI plan based on user goal and page context"""
        try:
            if not self.client:
                logger.warning("LLM: No OpenAI API key, using fallback plan generation")
                return self._generate_fallback_plan(user_goal, page_context)
            
            logger.info("LLM: Generating AI plan...")
            
            # Prepare context for LLM
            context_prompt = self._prepare_context_prompt(user_goal, page_context)
            
            # Call OpenAI API
            response = await self._call_openai_api(context_prompt)
            
            # Parse response
            plan = self._parse_llm_response(response, user_goal)
            
            logger.info(f"LLM: Generated plan with {len(plan.steps)} steps")
            return plan
            
        except Exception as e:
            logger.error(f"LLM: Error generating plan: {e}")
            return self._generate_fallback_plan(user_goal, page_context)
    
    def _prepare_context_prompt(self, user_goal: str, page_context: MCPPageContext) -> str:
        """Prepare context prompt for LLM"""
        prompt = f"""
You are an AI automation agent. Generate a step-by-step plan to achieve the user's goal.

USER GOAL: {user_goal}

PAGE CONTEXT:
- URL: {page_context.url}
- Title: {page_context.title}
- Page Type: {page_context.page_structure.get('page_type', 'unknown')}
- Has Search: {page_context.page_structure.get('has_search', False)}
- Has Products: {page_context.page_structure.get('has_products', False)}

AVAILABLE ELEMENTS:
"""
        
        # Add interactive elements
        for element in page_context.interactive_elements[:10]:  # Limit to first 10
            prompt += f"- {element['type']}: {element.get('text', element.get('placeholder', 'N/A'))}\n"
        
        prompt += """
Generate a JSON plan with the following structure:
{
    "steps": [
        {
            "action": "click|type|wait|navigate",
            "target": "element selector or text",
            "data": "text to type (if applicable)",
            "reasoning": "why this step is needed"
        }
    ],
    "confidence": 0.0-1.0,
    "reasoning": "overall strategy explanation",
    "expected_outcome": "what should happen"
}

Focus on:
1. Finding the right elements to interact with
2. Using appropriate selectors
3. Handling form inputs and buttons
4. Following logical flow
5. Being specific about element targeting

Return only the JSON, no other text.
"""
        
        return prompt
    
    async def _call_openai_api(self, prompt: str) -> str:
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert web automation agent. Generate precise, executable automation plans."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM: OpenAI API error: {e}")
            raise
    
    def _parse_llm_response(self, response: str, user_goal: str) -> AIPlan:
        """Parse LLM response into AIPlan"""
        try:
            # Clean response (remove markdown if present)
            response = response.strip()
            if response.startswith('```json'):
                response = response[7:]
            if response.endswith('```'):
                response = response[:-3]
            
            # Parse JSON
            plan_data = json.loads(response)
            
            return AIPlan(
                steps=plan_data.get('steps', []),
                confidence=plan_data.get('confidence', 0.8),
                reasoning=plan_data.get('reasoning', 'AI-generated plan'),
                expected_outcome=plan_data.get('expected_outcome', f'Complete: {user_goal}')
            )
            
        except Exception as e:
            logger.error(f"LLM: Error parsing response: {e}")
            return self._generate_fallback_plan(user_goal, None)
    
    def _generate_fallback_plan(self, user_goal: str, page_context: MCPPageContext = None) -> AIPlan:
        """Generate fallback plan when LLM is not available"""
        goal_lower = user_goal.lower()
        
        # Universal search strategy for all types of queries
        steps = [
            {
                "action": "type",
                "target": "input[name='q'], textarea[name='q'], input[type='search'], input[aria-label*='Search'], input[placeholder*='search' i], input[type='text']",
                "data": user_goal,
                "reasoning": "Type the search query into the search input"
            },
            {
                "action": "click",
                "target": "input[type='submit'], button[type='submit'], input[value*='Search'], button:has-text('Search'), [aria-label*='Search'], button",
                "data": "",
                "reasoning": "Submit the search"
            },
            {
                "action": "wait",
                "target": "",
                "data": "5",
                "reasoning": "Wait for results to load"
            }
        ]
        
        # Add specific actions based on query type
        if any(word in goal_lower for word in ['buy', 'purchase', 'add to cart']):
            steps.append({
                "action": "click",
                "target": "button:has-text('Add to Cart'), button:has-text('Buy'), [data-testid*='add-to-cart'], a:has-text('Buy')",
                "data": "",
                "reasoning": "Click on purchase or add to cart button if found"
            })
        elif any(word in goal_lower for word in ['watch', 'video', 'play']):
            steps.append({
                "action": "click",
                "target": "button:has-text('Play'), [data-testid*='play'], .play-button, video",
                "data": "",
                "reasoning": "Click play button for video content"
            })
        
        return AIPlan(
            steps=steps,
            confidence=0.8,
            reasoning="Universal fallback plan generated for any type of query",
            expected_outcome=f"Search and find results for: {user_goal}"
        )

class AIBrainMCP:
    """AI Brain with MCP Integration - Main orchestrator"""
    
    def __init__(self, openai_api_key: str = None):
        self.mcp_analyzer = MCPAnalyzer()
        self.llm_planner = LLMPlanner(openai_api_key)
        self.browser = None
        self.page = None
    
    async def start_browser(self):
        """Start browser for automation"""
        try:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # Show browser window so user can see automation
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-web-security',
                    '--disable-features=TranslateUI',
                    '--disable-ipc-flooding-protection',
                    '--no-first-run',
                    '--no-default-browser-check',
                    '--disable-default-apps',
                    '--disable-popup-blocking',
                    '--disable-prompt-on-repost',
                    '--disable-hang-monitor',
                    '--disable-client-side-phishing-detection',
                    '--disable-component-update',
                    '--disable-domain-reliability',
                    '--disable-features=AudioServiceOutOfProcess',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]
            )
            self.context = await self.browser.new_context(
                viewport={'width': 1366, 'height': 768},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='en-US',
                timezone_id='America/New_York',
                permissions=['geolocation'],
                extra_http_headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
            )
            self.page = await self.context.new_page()
            
            # Add stealth scripts to avoid detection
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                window.chrome = {
                    runtime: {},
                };
            """)
            
            logger.info("AI Brain: Browser started with visible window")
            return True
        except Exception as e:
            logger.error(f"AI Brain: Failed to start browser: {e}")
            return False
    
    async def execute_ai_automation(self, user_goal: str, website: str) -> Dict[str, Any]:
        """Execute AI-powered automation with MCP integration"""
        try:
            logger.info(f"AI Brain: Starting automation for goal: {user_goal}")
            
            # Step 1: Navigate to website
            await self.page.goto(website, wait_until='domcontentloaded')
            await asyncio.sleep(2)
            
            # Step 2: MCP Analysis - Get page context
            logger.info("AI Brain: MCP analyzing page context...")
            page_context = await self.mcp_analyzer.analyze_page_context(self.page)
            
            # Step 3: LLM Planning - Generate AI plan
            logger.info("AI Brain: LLM generating execution plan...")
            ai_plan = await self.llm_planner.generate_plan(user_goal, page_context)
            
            # Step 4: Execute AI plan
            logger.info(f"AI Brain: Executing {len(ai_plan.steps)} steps from AI plan...")
            execution_results = await self._execute_ai_plan(ai_plan)
            
            # Step 5: Extract results (ensure browser is still open)
            if self.page and not self.page.is_closed():
                final_results = await self._extract_final_results()
            else:
                logger.warning("AI Brain: Browser was closed, using fallback results")
                final_results = {
                    'page_title': 'Browser Closed',
                    'page_url': 'N/A',
                    'results': [],
                    'result_count': 0,
                    'extraction_method': 'fallback_due_to_browser_close'
                }
            
            return {
                'success': True,
                'user_goal': user_goal,
                'ai_plan': {
                    'steps': ai_plan.steps,
                    'confidence': ai_plan.confidence,
                    'reasoning': ai_plan.reasoning,
                    'expected_outcome': ai_plan.expected_outcome
                },
                'execution_results': execution_results,
                'final_results': final_results,
                'mcp_context': {
                    'url': page_context.url,
                    'title': page_context.title,
                    'elements_found': len(page_context.elements),
                    'interactive_elements': len(page_context.interactive_elements),
                    'page_type': page_context.page_structure.get('page_type', 'unknown')
                }
            }
            
        except Exception as e:
            logger.error(f"AI Brain: Automation failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'user_goal': user_goal
            }
    
    async def _execute_ai_plan(self, ai_plan: AIPlan) -> List[Dict[str, Any]]:
        """Execute the AI-generated plan"""
        execution_results = []
        
        for i, step in enumerate(ai_plan.steps):
            try:
                logger.info(f"AI Brain: Executing step {i+1}: {step['action']} - {step['reasoning']}")
                
                if step['action'] == 'click':
                    await self._execute_click(step)
                elif step['action'] == 'type':
                    await self._execute_type(step)
                elif step['action'] == 'wait':
                    await self._execute_wait(step)
                elif step['action'] == 'navigate':
                    await self._execute_navigate(step)
                
                execution_results.append({
                    'step': i + 1,
                    'action': step['action'],
                    'success': True,
                    'reasoning': step['reasoning']
                })
                
                await asyncio.sleep(1)  # Brief pause between steps
                
            except Exception as e:
                logger.error(f"AI Brain: Step {i+1} failed: {e}")
                execution_results.append({
                    'step': i + 1,
                    'action': step['action'],
                    'success': False,
                    'error': str(e),
                    'reasoning': step['reasoning']
                })
        
        return execution_results
    
    async def _execute_click(self, step: Dict[str, Any]):
        """Execute click action"""
        target = step['target']
        if target:
            # Try multiple selectors
            selectors = target.split(', ')
            element = None
            for selector in selectors:
                try:
                    element = await self.page.wait_for_selector(selector.strip(), timeout=3000)
                    if element:
                        break
                except:
                    continue
            
            if element:
                await element.click()
            else:
                # Try pressing Enter as fallback
                await self.page.keyboard.press('Enter')
    
    async def _execute_type(self, step: Dict[str, Any]):
        """Execute type action"""
        target = step['target']
        data = step['data']
        if target and data:
            # Try multiple selectors
            selectors = target.split(', ')
            element = None
            for selector in selectors:
                try:
                    element = await self.page.wait_for_selector(selector.strip(), timeout=3000)
                    if element:
                        break
                except:
                    continue
            
            if element:
                await element.click()
                await element.fill('')
                await element.fill(data)
            else:
                # Try typing directly into the page
                await self.page.keyboard.type(data)
    
    async def _execute_wait(self, step: Dict[str, Any]):
        """Execute wait action"""
        duration = float(step['data']) if step['data'] else 2
        await asyncio.sleep(duration)
    
    async def _execute_navigate(self, step: Dict[str, Any]):
        """Execute navigate action"""
        url = step['data']
        if url:
            await self.page.goto(url)
    
    async def _extract_final_results(self) -> Dict[str, Any]:
        """Extract final results from the page"""
        try:
            # Get page title and URL
            title = await self.page.title()
            url = self.page.url
            
            # Wait for page to load completely
            await asyncio.sleep(3)
            
            # Try to extract meaningful content
            results = []
            
            # Strategy 1: DuckDuckGo search results (most reliable)
            try:
                ddg_results = await self.page.query_selector_all('[data-testid="result"]')
                if ddg_results:
                    logger.info(f"Found {len(ddg_results)} DuckDuckGo results")
                    for i, result in enumerate(ddg_results[:5]):
                        try:
                            # Get title and link from the main link
                            title_link = await result.query_selector('h2 a, .result__title a, a[data-testid="result-title-a"]')
                            if title_link:
                                title_text = await title_link.inner_text()
                                link = await title_link.get_attribute('href')
                                
                                # Get snippet
                                snippet_elem = await result.query_selector('.result__snippet, .result__body, [data-result="snippet"]')
                                snippet = await snippet_elem.inner_text() if snippet_elem else ""
                                
                                if title_text and len(title_text.strip()) > 3 and link:
                                    # Clean up the link to ensure it's a proper URL
                                    if link.startswith('/'):
                                        link = f"https://duckduckgo.com{link}"
                                    elif not link.startswith('http'):
                                        link = f"https://{link}"
                                    
                                    results.append({
                                        'title': title_text.strip(),
                                        'snippet': snippet.strip()[:200] if snippet else "",
                                        'link': link,
                                        'type': 'search_result'
                                    })
                        except Exception as e:
                            logger.warning(f"Error extracting DuckDuckGo result {i}: {e}")
                            continue
            except Exception as e:
                logger.warning(f"DuckDuckGo extraction failed: {e}")
            
            # Strategy 2: Google search results
            if not results:
                try:
                    google_results = await self.page.query_selector_all('.g')
                    if google_results:
                        logger.info(f"Found {len(google_results)} Google results")
                        for i, result in enumerate(google_results[:5]):
                            try:
                                # Get title and link
                                title_link = await result.query_selector('h3 a, .yuRUbf a')
                                if title_link:
                                    title_text = await title_link.inner_text()
                                    link = await title_link.get_attribute('href')
                                    
                                    # Get snippet
                                    snippet_elem = await result.query_selector('.VwiC3b, .s3v9rd, .IsZvec')
                                    snippet = await snippet_elem.inner_text() if snippet_elem else ""
                                    
                                    if title_text and len(title_text.strip()) > 3 and link:
                                        results.append({
                                            'title': title_text.strip(),
                                            'snippet': snippet.strip()[:200] if snippet else "",
                                            'link': link,
                                            'type': 'search_result'
                                        })
                            except Exception as e:
                                logger.warning(f"Error extracting Google result {i}: {e}")
                                continue
                except Exception as e:
                    logger.warning(f"Google extraction failed: {e}")
            
            # Strategy 3: Amazon product results
            if not results:
                try:
                    amazon_results = await self.page.query_selector_all('[data-component-type="s-search-result"]')
                    if amazon_results:
                        logger.info(f"Found {len(amazon_results)} Amazon results")
                        for i, result in enumerate(amazon_results[:5]):
                            try:
                                # Get title and link
                                title_link = await result.query_selector('h2 a')
                                if title_link:
                                    title_text = await title_link.inner_text()
                                    link = await title_link.get_attribute('href')
                                    
                                    # Get price
                                    price_elem = await result.query_selector('.a-price-whole, .a-price .a-offscreen')
                                    price = await price_elem.inner_text() if price_elem else ""
                                    
                                    # Get rating
                                    rating_elem = await result.query_selector('.a-icon-alt')
                                    rating = await rating_elem.inner_text() if rating_elem else ""
                                    
                                    if title_text and len(title_text.strip()) > 3 and link:
                                        # Clean up Amazon link
                                        if link.startswith('/'):
                                            link = f"https://amazon.com{link}"
                                        
                                        results.append({
                                            'title': title_text.strip(),
                                            'price': price.strip() if price else "",
                                            'rating': rating.strip() if rating else "",
                                            'link': link,
                                            'type': 'product'
                                        })
                            except Exception as e:
                                logger.warning(f"Error extracting Amazon result {i}: {e}")
                                continue
                except Exception as e:
                    logger.warning(f"Amazon extraction failed: {e}")
            
            # Strategy 4: Generic search results (any site)
            if not results:
                try:
                    # Look for common search result patterns
                    search_results = await self.page.query_selector_all('a[href*="http"]:not([href*="' + url.split('/')[2] + '"])')
                    if search_results:
                        logger.info(f"Found {len(search_results)} generic results")
                        for i, result in enumerate(search_results[:5]):
                            try:
                                link = await result.get_attribute('href')
                                title_text = await result.inner_text()
                                
                                if link and title_text and len(title_text.strip()) > 3 and len(title_text.strip()) < 100:
                                    results.append({
                                        'title': title_text.strip(),
                                        'link': link,
                                        'type': 'search_result'
                                    })
                            except:
                                continue
                except Exception as e:
                    logger.warning(f"Generic extraction failed: {e}")
            
            # Strategy 5: Fallback - provide page content
            if not results:
                try:
                    body_text = await self.page.inner_text('body')
                    if body_text and len(body_text.strip()) > 50:
                        results.append({
                            'title': f"Page Content: {title}",
                            'type': 'page_content',
                            'content': body_text.strip()[:500] + "..." if len(body_text.strip()) > 500 else body_text.strip()
                        })
                except:
                    pass
            
            logger.info(f"Extracted {len(results)} results")
            return {
                'page_title': title,
                'page_url': url,
                'results': results,
                'result_count': len(results),
                'extraction_method': 'real_web_automation'
            }
            
        except Exception as e:
            logger.error(f"AI Brain: Error extracting results: {e}")
            return {'error': str(e)}
    
    async def close_browser(self):
        """Close browser"""
        try:
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
            logger.info("AI Brain: Browser closed")
        except Exception as e:
            logger.error(f"AI Brain: Error closing browser: {e}")

# Test function
async def test_ai_brain_mcp():
    """Test the AI Brain with MCP integration"""
    print("Testing AI Brain with MCP Integration...")
    
    ai_brain = AIBrainMCP()
    
    try:
        # Start browser
        if await ai_brain.start_browser():
            # Test automation
            result = await ai_brain.execute_ai_automation(
                "find cheapest halloween dress",
                "https://duckduckgo.com"
            )
            
            print(f"Result: {result}")
        else:
            print("Failed to start browser")
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        await ai_brain.close_browser()

if __name__ == "__main__":
    asyncio.run(test_ai_brain_mcp())
