"""
Database module for SQLite operations.
Handles database connection, table initialization, and logging operations.
"""

import sqlite3
import aiosqlite
import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path


class DatabaseManager:
    """
    Manages SQLite database operations for translation logging.
    """
    
    def __init__(self, db_path: str = "translation_logs.db"):
        """
        Initialize database manager.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self._ensure_db_directory()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    async def initialize_database(self):
        """
        Initialize the database and create necessary tables.
        """
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS translation_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_text TEXT NOT NULL,
                    translated_text TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    timestamp DATETIME NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for better query performance
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON translation_logs(timestamp)
            """)
            
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_target_language 
                ON translation_logs(target_language)
            """)
            
            await db.commit()
    
    async def log_translation(
        self, 
        original_text: str, 
        translated_text: str, 
        target_language: str,
        timestamp: Optional[datetime] = None
    ) -> int:
        """
        Log a translation request to the database.
        
        Args:
            original_text (str): The original text
            translated_text (str): The translated text
            target_language (str): The target language code
            timestamp (Optional[datetime]): Custom timestamp, defaults to now
            
        Returns:
            int: The ID of the inserted record
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO translation_logs 
                (original_text, translated_text, target_language, timestamp)
                VALUES (?, ?, ?, ?)
            """, (original_text, translated_text, target_language, timestamp))
            
            await db.commit()
            return cursor.lastrowid
    
    async def log_bulk_translation(
        self, 
        translations: List[Dict[str, str]],
        timestamp: Optional[datetime] = None
    ) -> List[int]:
        """
        Log multiple translation requests to the database.
        
        Args:
            translations (List[Dict[str, str]]): List of translation dictionaries
            timestamp (Optional[datetime]): Custom timestamp, defaults to now
            
        Returns:
            List[int]: List of inserted record IDs
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        record_ids = []
        
        async with aiosqlite.connect(self.db_path) as db:
            for translation in translations:
                cursor = await db.execute("""
                    INSERT INTO translation_logs 
                    (original_text, translated_text, target_language, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (
                    translation['original_text'],
                    translation['translated_text'],
                    translation['target_language'],
                    timestamp
                ))
                record_ids.append(cursor.lastrowid)
            
            await db.commit()
        
        return record_ids
    
    async def get_translation_logs(
        self, 
        limit: int = 100, 
        offset: int = 0,
        target_language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve translation logs from the database.
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            target_language (Optional[str]): Filter by target language
            
        Returns:
            List[Dict[str, Any]]: List of translation log records
        """
        query = """
            SELECT id, original_text, translated_text, target_language, 
                   timestamp, created_at
            FROM translation_logs
        """
        params = []
        
        if target_language:
            query += " WHERE target_language = ?"
            params.append(target_language)
        
        query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(row) for row in rows]
    
    async def get_translation_stats(self) -> Dict[str, Any]:
        """
        Get translation statistics from the database.
        
        Returns:
            Dict[str, Any]: Statistics about translations
        """
        async with aiosqlite.connect(self.db_path) as db:
            # Total translations
            async with db.execute("SELECT COUNT(*) as total FROM translation_logs") as cursor:
                total_result = await cursor.fetchone()
                total_translations = total_result[0] if total_result else 0
            
            # Translations by language
            async with db.execute("""
                SELECT target_language, COUNT(*) as count 
                FROM translation_logs 
                GROUP BY target_language 
                ORDER BY count DESC
            """) as cursor:
                language_stats = await cursor.fetchall()
            
            # Recent activity (last 24 hours)
            async with db.execute("""
                SELECT COUNT(*) as recent_count 
                FROM translation_logs 
                WHERE timestamp >= datetime('now', '-1 day')
            """) as cursor:
                recent_result = await cursor.fetchone()
                recent_translations = recent_result[0] if recent_result else 0
            
            return {
                "total_translations": total_translations,
                "recent_translations_24h": recent_translations,
                "translations_by_language": [
                    {"language": row[0], "count": row[1]} 
                    for row in language_stats
                ]
            }
    
    async def close(self):
        """
        Close database connections (placeholder for cleanup if needed).
        """
        pass


# Global database manager instance
db_manager = DatabaseManager()