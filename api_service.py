"""
FastAPI Service - Web API for remote automation control
This module provides REST API endpoints for automation tasks.
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from core_robot import WebRobot, AutomationResult
from ai_brain import AIBrain
from database import get_db, AutomationTask, AutomationSession, init_database

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Cali Automation API",
    description="Web automation service with AI-powered task execution",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_database()

# Pydantic models for API
class TaskRequest(BaseModel):
    task_name: str
    description: Optional[str] = None
    task_type: str = "core"  # "core" or "ai"
    user_goal: Optional[str] = None
    page_url: Optional[str] = None

class AIBrainRequest(BaseModel):
    user_goal: str
    page_url: str

class TaskResponse(BaseModel):
    task_id: int
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

# Global variables for background tasks
background_tasks: Dict[int, asyncio.Task] = {}

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Cali Automation API",
        "version": "1.0.0",
        "endpoints": {
            "core_automation": "/automate/core",
            "ai_automation": "/automate/ai",
            "task_status": "/tasks/{task_id}",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.post("/automate/core", response_model=TaskResponse)
async def core_automation(request: TaskRequest, background_tasks: BackgroundTasks):
    """Execute core automation task"""
    try:
        # Create task record
        db = next(get_db())
        task = AutomationTask(
            task_name=request.task_name,
            description=request.description,
            status="running",
            user_goal=request.user_goal
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Start background task
        background_tasks.add_task(execute_core_task, task.id, request)
        
        return TaskResponse(
            task_id=task.id,
            status="running",
            message="Core automation task started",
            data={"task_name": request.task_name}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start task: {str(e)}")

@app.post("/automate/ai", response_model=TaskResponse)
async def ai_automation(request: AIBrainRequest, background_tasks: BackgroundTasks):
    """Execute AI-powered automation task"""
    try:
        # Check for OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        # Create task record
        db = next(get_db())
        task = AutomationTask(
            task_name="AI Automation",
            description=f"AI task: {request.user_goal}",
            status="running",
            user_goal=request.user_goal
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # Start background task
        background_tasks.add_task(execute_ai_task, task.id, request)
        
        return TaskResponse(
            task_id=task.id,
            status="running",
            message="AI automation task started",
            data={"user_goal": request.user_goal, "page_url": request.page_url}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start AI task: {str(e)}")

@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: int):
    """Get task status and results"""
    try:
        db = next(get_db())
        task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Parse result data if available
        result_data = None
        if task.result_data:
            try:
                result_data = json.loads(task.result_data)
            except json.JSONDecodeError:
                result_data = {"raw_data": task.result_data}
        
        return TaskResponse(
            task_id=task.id,
            status=task.status,
            message=f"Task {task.status}",
            data={
                "task_name": task.task_name,
                "description": task.description,
                "created_at": task.created_at.isoformat(),
                "completed_at": task.completed_at.isoformat() if task.completed_at else None,
                "result_data": result_data,
                "error_message": task.error_message
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")

@app.get("/tasks")
async def list_tasks():
    """List all tasks"""
    try:
        db = next(get_db())
        tasks = db.query(AutomationTask).order_by(AutomationTask.created_at.desc()).limit(50).all()
        
        return {
            "tasks": [
                {
                    "id": task.id,
                    "task_name": task.task_name,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                    "completed_at": task.completed_at.isoformat() if task.completed_at else None
                }
                for task in tasks
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list tasks: {str(e)}")

async def execute_core_task(task_id: int, request: TaskRequest):
    """Execute core automation task in background"""
    try:
        db = next(get_db())
        task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
        
        if not task:
            return
        
        # Execute core automation
        robot = WebRobot(headless=True)
        result = await robot.execute_example_task()
        
        # Update task status
        task.status = "completed" if result.success else "failed"
        task.completed_at = datetime.utcnow()
        task.result_data = json.dumps({
            "success": result.success,
            "message": result.message,
            "data": result.data
        })
        if result.error:
            task.error_message = result.error
        
        db.commit()
        
    except Exception as e:
        # Update task with error
        db = next(get_db())
        task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
        if task:
            task.status = "failed"
            task.completed_at = datetime.utcnow()
            task.error_message = str(e)
            db.commit()

async def execute_ai_task(task_id: int, request: AIBrainRequest):
    """Execute AI automation task in background"""
    try:
        db = next(get_db())
        task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
        
        if not task:
            return
        
        # Execute AI automation
        api_key = os.getenv('OPENAI_API_KEY')
        ai_brain = AIBrain(api_key)
        result = await ai_brain.execute_ai_task(request.user_goal, request.page_url)
        
        # Update task status
        task.status = "completed" if result.success else "failed"
        task.completed_at = datetime.utcnow()
        task.result_data = json.dumps({
            "success": result.success,
            "message": result.message,
            "data": result.data
        })
        if result.error:
            task.error_message = result.error
        
        db.commit()
        
    except Exception as e:
        # Update task with error
        db = next(get_db())
        task = db.query(AutomationTask).filter(AutomationTask.id == task_id).first()
        if task:
            task.status = "failed"
            task.completed_at = datetime.utcnow()
            task.error_message = str(e)
            db.commit()

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv('API_HOST', '0.0.0.0')
    port = int(os.getenv('API_PORT', 8000))
    
    print(f"🚀 Starting Cali Automation API on {host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    
    uvicorn.run(app, host=host, port=port)
