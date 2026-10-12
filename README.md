# Cali Automation

Cali Automation is an AI-driven web automation platform that turns plain-language goals into automated web actions. You describe what you want, such as finding products, researching news, or searching for jobs, and the system selects a suitable website, performs real browser automation with Playwright, and returns structured, clickable results.

## Core Features

### Goal Understanding
- Accepts natural-language goals across multiple categories: shopping, news, travel, jobs, education, and more.
- No scripting or configuration required: the goal is interpreted automatically.

### Intelligent Decision-Making
- Selects the right website for each task.
- Generates a step-by-step plan for interacting with that website (with OpenAI when `OPENAI_API_KEY` is set, otherwise with a built-in rule-based planner).
- Analyzes the page structure before planning.
- Executes each step while handling errors gracefully.

### Browser-Level Automation
- Uses real browsers through Playwright to perform visible, traceable actions (Chromium for the web API; `universal_automation.py` can also use Firefox and WebKit).
- Includes stealth and anti-detection measures.
- Captures real-world results from live web pages.

### Usable Results
- Extracts links, titles, prices, ratings, and descriptions.
- Delivers results in a structured, clickable format.
- Uses fallback extraction methods when primary selectors fail.

## System Architecture

1. **AI Brain with MCP-style page analysis** (`ai_brain_mcp_integration.py`): intent analysis, planning, and step-by-step automation logic.
2. **Web API server** (`web_api.py`): FastAPI REST API for task submission and monitoring:
   - `POST /automate/goal`: submit a new goal
   - `POST /automate`: run the fixed robot driver task (`robot_driver_complete.py`) on books.toscrape.com
   - `GET /tasks/{task_id}`: fetch task results
   - `GET /tasks`: list all tasks
   - `GET /health`: health check
3. **Web interface** (`goal_interface.html`, served by `start_web_interface.py`): frontend for entering goals, tracking progress, and viewing results.
4. **Universal automation engine** (`universal_automation.py`): a standalone automation engine with multi-browser support, fallback selectors and stealth techniques, used by `test_automation.py` and `debug_automation.py`.

## Getting Started

### Requirements
- Python 3.8+
- pip
- Internet connection

### Installation

```bash
git clone https://github.com/bhavanagoud111/The-Robot-driver.git
cd The-Robot-driver
./setup.sh
```

`setup.sh` installs the Python dependencies and Playwright browsers and creates `.env` from `env.example`.

### Running

The API server and the web interface are separate processes:

```bash
# Terminal 1: API server on http://localhost:8000
python3 web_api.py

# Terminal 2: web interface on http://localhost:8081
python3 start_web_interface.py
```

Then open http://localhost:8081.

### First Run
1. Open the local web interface.
2. Enter a goal like "Find the best laptops under $1000."
3. Start the automation and watch the browser perform each step.
4. Review the extracted links and summaries.

## Example Usage (API)

Submit a goal:

```bash
curl -X POST http://localhost:8000/automate/goal \
  -H "Content-Type: application/json" \
  -d '{"user_goal": "find cheapest halloween dress"}'
```

Check task results:

```bash
curl http://localhost:8000/tasks/{task_id}
```

Interactive API docs are available at http://localhost:8000/docs.

## AI Processing Pipeline

1. **Goal analysis**: understands the user's intent.
2. **Website selection**: chooses a suitable site (e.g. DuckDuckGo, LinkedIn Jobs, Skyscanner, YouTube).
3. **Plan generation**: builds a browser interaction sequence (type, click, wait).
4. **Execution**: performs the automation with Playwright.
5. **Result extraction**: captures and structures the final output.

## Configuration

Copy `env.example` to `.env` (done by `setup.sh`):

```env
OPENAI_API_KEY=          # optional; enables LLM-generated plans
API_HOST=0.0.0.0
API_PORT=8000
WEB_PORT=8081
HEADLESS=false           # set to true where no display is available
```

`goal_interface.html` calls the API at `http://localhost:8000`; update the URLs in that file if you change `API_PORT`. The `DB_*` settings are only used by the older `api_service.py` / `database.py` code path.

### Common Fixes
- Port in use: change `API_PORT` or `WEB_PORT`.
- Browser errors: reinstall with `playwright install --force`.
- Permission issues: `chmod +x setup.sh`.

## Docker

```bash
docker build -t cali-automation .
docker run -p 8000:8000 cali-automation
```

The container runs `web_api.py` with the browser in headless mode.

See [SETUP.md](SETUP.md) for a detailed setup and troubleshooting guide.

## Example Use Cases
- **E-commerce**: compare prices and reviews, find deals.
- **Research and news**: gather current headlines and research results.
- **Careers**: search for job openings.
- **Travel**: look up flights and travel offers.

## Future Development
- User accounts and saved automations.
- Scheduling and recurring tasks.
- Faster element detection and better failure recovery.
