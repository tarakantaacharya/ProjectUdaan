import sqlite3
import logging
from datetime import datetime
from typing import List, Dict, Optional
import json

logger = logging.getLogger(__name__)

DATABASE_PATH = "translations.db"

def init_db():
    """Initialize the database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translations (
                id TEXT PRIMARY KEY,
                original_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                source_language TEXT NOT NULL,
                target_language TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise

def get_translation_history(limit: int = 100) -> List[Dict]:
    """Get translation history from database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM translations 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        history = []
        for row in results:
            history.append({
                'id': row[0],
                'original_text': row[1],
                'translated_text': row[2],
                'source_language': row[3],
                'target_language': row[4],
                'timestamp': row[5],
                'created_at': row[6]
            })
        
        return history
        
    except Exception as e:
        logger.error(f"Failed to get translation history: {str(e)}")
        return []