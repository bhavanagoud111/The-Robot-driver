"""
Database models and connection for the automation system
"""

import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'cali_automation')
DB_USER = os.getenv('DB_USER', 'cali_user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'cali_password')

# Create database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AutomationTask(Base):
    """Model for storing automation tasks"""
    __tablename__ = "automation_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    result_data = Column(Text, nullable=True)  # JSON string of results
    error_message = Column(Text, nullable=True)
    user_goal = Column(Text, nullable=True)  # For AI Brain tasks

class AutomationSession(Base):
    """Model for storing automation sessions"""
    __tablename__ = "automation_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, nullable=False)
    session_data = Column(Text, nullable=True)  # JSON string of session data
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    success = Column(Boolean, default=False)

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        return db
    finally:
        pass

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def init_database():
    """Initialize the database with tables"""
    try:
        create_tables()
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Failed to create database tables: {e}")
        raise
