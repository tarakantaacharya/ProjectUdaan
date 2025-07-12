from fastapi import APIRouter
from datetime import datetime
import sqlite3
from services.database_service import DATABASE_PATH

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connectivity
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "service": "Translation Microservice",
        "version": "1.0.0",
        "database": db_status
    }