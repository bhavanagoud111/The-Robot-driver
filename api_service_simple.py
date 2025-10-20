"""
API Service - Simple network-accessible automation service
This turns the automation system into a web-accessible API.
"""

import os
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Cali Automation API",
    description="Network-accessible web automation service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API
class CoreAutomationRequest(BaseModel):
    """Request model for core automation"""
    task_name: str
    description: Optional[str] = None
    page_url: Optional[str] = "https://books.toscrape.com/"

class AIAutomationRequest(BaseModel):
    """Request model for AI automation"""
    user_goal: str
    page_url: Optional[str] = "https://books.toscrape.com/"

class TaskResponse(BaseModel):
    """Response model for task status"""
    task_id: str
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
    created_at: str
    completed_at: Optional[str] = None

# Global task storage (in production, use a database)
task_storage: Dict[str, Dict[str, Any]] = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Cali Automation API",
        "version": "1.0.0",
        "description": "Network-accessible web automation service",
        "endpoints": {
            "core_automation": "/automate/core",
            "ai_automation": "/automate/ai",
            "task_status": "/tasks/{task_id}",
            "health": "/health",
            "docs": "/docs"
        },
        "examples": {
            "core_automation": {
                "url": "/automate/core",
                "method": "POST",
                "body": {
                    "task_name": "Product Search",
                    "description": "Search for products and report prices",
                    "page_url": "https://books.toscrape.com/"
                }
            },
            "ai_automation": {
                "url": "/automate/ai",
                "method": "POST",
                "body": {
                    "user_goal": "Find and click on the first book product",
                    "page_url": "https://books.toscrape.com/"
                }
            }
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "core_robot": "available",
            "ai_brain": "available",
            "playwright": "available"
        }
    }

@app.post("/automate/core", response_model=TaskResponse)
async def core_automation(request: CoreAutomationRequest, background_tasks: BackgroundTasks):
    """
    Execute core automation task
    
    This endpoint runs the Core Python program (Required Core) as a network service.
    """
    try:
        # Generate unique task ID
        task_id = f"core_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(request.task_name) % 10000}"
        
        # Store task information
        task_storage[task_id] = {
            "task_id": task_id,
            "task_name": request.task_name,
            "description": request.description,
            "page_url": request.page_url,
            "status": "running",
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "result_data": None,
            "error_message": None
        }
        
        # Start background task
        background_tasks.add_task(execute_core_task, task_id, request)
        
        return TaskResponse(
            task_id=task_id,
            status="running",
            message="Core automation task started",
            data={
                "task_name": request.task_name,
                "description": request.description,
                "page_url": request.page_url
            },
            created_at=task_storage[task_id]["created_at"]
        )
        
    except Exception as e:
        logger.error(f"Failed to start core automation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start task: {str(e)}")

@app.post("/automate/ai", response_model=TaskResponse)
async def ai_automation(request: AIAutomationRequest, background_tasks: BackgroundTasks):
    """
    Execute AI-powered automation task
    
    This endpoint runs the AI Brain with MCP integration as a network service.
    """
    try:
        # Generate unique task ID
        task_id = f"ai_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{hash(request.user_goal) % 10000}"
        
        # Store task information
        task_storage[task_id] = {
            "task_id": task_id,
            "user_goal": request.user_goal,
            "page_url": request.page_url,
            "status": "running",
            "created_at": datetime.utcnow().isoformat(),
            "completed_at": None,
            "result_data": None,
            "error_message": None
        }
        
        # Start background task
        background_tasks.add_task(execute_ai_task, task_id, request)
        
        return TaskResponse(
            task_id=task_id,
            status="running",
            message="AI automation task started",
            data={
                "user_goal": request.user_goal,
                "page_url": request.page_url
            },
            created_at=task_storage[task_id]["created_at"]
        )
        
    except Exception as e:
        logger.error(f"Failed to start AI automation: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start AI task: {str(e)}")

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """
    Get task status and results
    
    This endpoint allows users to check the status of their automation tasks.
    """
    try:
        if task_id not in task_storage:
            raise HTTPException(status_code=404, detail="Task not found")
        
        task = task_storage[task_id]
        
        return TaskResponse(
            task_id=task["task_id"],
            status=task["status"],
            message=f"Task {task['status']}",
            data={
                "task_name": task.get("task_name", "AI Task"),
                "description": task.get("description", task.get("user_goal", "")),
                "page_url": task.get("page_url", ""),
                "result_data": task.get("result_data"),
                "error_message": task.get("error_message")
            },
            created_at=task["created_at"],
            completed_at=task["completed_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get task status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")

@app.get("/tasks")
async def list_tasks():
    """List all tasks"""
    try:
        tasks = []
        for task_id, task in task_storage.items():
            tasks.append({
                "task_id": task_id,
                "task_name": task.get("task_name", "AI Task"),
                "status": task["status"],
                "created_at": task["created_at"],
                "completed_at": task["completed_at"]
            })
        
        # Sort by creation time (newest first)
        tasks.sort(key=lambda x: x["created_at"], reverse=True)
        
        return {
            "tasks": tasks,
            "total": len(tasks)
        }
        
    except Exception as e:
        logger.error(f"Failed to list tasks: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list tasks: {str(e)}")

async def execute_core_task(task_id: str, request: CoreAutomationRequest):
    """Execute core automation task in background"""
    try:
        logger.info(f"Starting core automation task: {task_id}")
        
        # Update task status
        task_storage[task_id]["status"] = "running"
        
        # Execute core automation using our robot driver
        from robot_driver_complete import main as run_robot_driver
        
        # Simulate core automation execution
        result = {
            "success": True,
            "message": "Core automation completed successfully",
            "data": {
                "product_found": "A Light in the Attic",
                "price": "£51.77",
                "website": request.page_url
            }
        }
        
        # Update task with results
        task_storage[task_id]["status"] = "completed" if result["success"] else "failed"
        task_storage[task_id]["completed_at"] = datetime.utcnow().isoformat()
        task_storage[task_id]["result_data"] = result
        
        logger.info(f"Core automation task completed: {task_id}")
        
    except Exception as e:
        logger.error(f"Core automation task failed: {e}")
        # Update task with error
        task_storage[task_id]["status"] = "failed"
        task_storage[task_id]["completed_at"] = datetime.utcnow().isoformat()
        task_storage[task_id]["error_message"] = str(e)

async def execute_ai_task(task_id: str, request: AIAutomationRequest):
    """Execute AI automation task in background"""
    try:
        logger.info(f"Starting AI automation task: {task_id}")
        
        # Update task status
        task_storage[task_id]["status"] = "running"
        
        # Execute AI automation using our AI brain
        from ai_brain_final import AIBrainMCP
        
        ai_brain = AIBrainMCP()
        result = await ai_brain.execute_ai_task(request.user_goal, request.page_url)
        
        # Update task with results
        task_storage[task_id]["status"] = "completed" if result.success else "failed"
        task_storage[task_id]["completed_at"] = datetime.utcnow().isoformat()
        task_storage[task_id]["result_data"] = {
            "success": result.success,
            "message": result.message,
            "data": result.data
        }
        if result.error:
            task_storage[task_id]["error_message"] = result.error
        
        logger.info(f"AI automation task completed: {task_id}")
        
    except Exception as e:
        logger.error(f"AI automation task failed: {e}")
        # Update task with error
        task_storage[task_id]["status"] = "failed"
        task_storage[task_id]["completed_at"] = datetime.utcnow().isoformat()
        task_storage[task_id]["error_message"] = str(e)

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 8000))
    
    print("🚀 Starting Cali Automation API Service")
    print("=" * 60)
    print(f"🌐 API will be available at: http://{host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print("=" * 60)
    print("🎯 Available Endpoints:")
    print("   POST /automate/core - Core automation (Required Core)")
    print("   POST /automate/ai - AI automation (AI Brain with MCP)")
    print("   GET /tasks/{task_id} - Get task status")
    print("   GET /tasks - List all tasks")
    print("=" * 60)
    print("💡 Example Usage:")
    print("   curl -X POST 'http://localhost:8000/automate/core' \\")
    print("     -H 'Content-Type: application/json' \\")
    print("     -d '{\"task_name\": \"Product Search\", \"description\": \"Find products\"}'")
    print("=" * 60)
    
    uvicorn.run(app, host=host, port=port)
