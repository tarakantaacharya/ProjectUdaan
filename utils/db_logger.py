import sqlite3
from datetime import datetime
import logging

DATABASE_PATH = "translations.db"  # Adjust if needed
logger = logging.getLogger(__name__)

def log_translation(translation_id: str, original_text: str, translated_text: str,
                   source_language: str, target_language: str, timestamp: datetime):
    """Log a translation to the database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO translations 
            (id, original_text, translated_text, source_language, target_language, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (translation_id, original_text, translated_text, source_language, target_language, timestamp))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log translation: {str(e)}")
