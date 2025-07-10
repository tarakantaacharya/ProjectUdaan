"""
Logging service for translation requests.
Handles logging translation requests to SQLite database or in-memory store.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from ..db.database import db_manager


class TranslationLogger:
    """
    Service for logging translation requests and managing translation history.
    """
    
    def __init__(self):
        """Initialize the translation logger."""
        self.db_manager = db_manager
        self._in_memory_logs = []  # Fallback for when database is not available
        self._use_database = True
    
    async def initialize(self):
        """
        Initialize the logger and database.
        """
        try:
            await self.db_manager.initialize_database()
            self._use_database = True
        except Exception as e:
            print(f"Warning: Could not initialize database, using in-memory logging: {e}")
            self._use_database = False
    
    async def log_single_translation(
        self,
        original_text: str,
        translated_text: str,
        target_language: str,
        timestamp: Optional[datetime] = None
    ) -> bool:
        """
        Log a single translation request.
        
        Args:
            original_text (str): The original text
            translated_text (str): The translated text
            target_language (str): The target language code
            timestamp (Optional[datetime]): Custom timestamp, defaults to now
            
        Returns:
            bool: True if logged successfully, False otherwise
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        log_entry = {
            "original_text": original_text,
            "translated_text": translated_text,
            "target_language": target_language,
            "timestamp": timestamp.isoformat()
        }
        
        try:
            if self._use_database:
                await self.db_manager.log_translation(
                    original_text, translated_text, target_language, timestamp
                )
            else:
                # Fallback to in-memory logging
                self._in_memory_logs.append(log_entry)
                # Keep only last 1000 entries to prevent memory issues
                if len(self._in_memory_logs) > 1000:
                    self._in_memory_logs = self._in_memory_logs[-1000:]
            
            return True
            
        except Exception as e:
            print(f"Error logging translation: {e}")
            # Try fallback to in-memory if database fails
            if self._use_database:
                try:
                    self._in_memory_logs.append(log_entry)
                    self._use_database = False
                    print("Switched to in-memory logging due to database error")
                    return True
                except Exception as fallback_error:
                    print(f"Error in fallback logging: {fallback_error}")
            
            return False
    
    async def log_bulk_translation(
        self,
        translations: List[Dict[str, str]],
        timestamp: Optional[datetime] = None
    ) -> bool:
        """
        Log multiple translation requests.
        
        Args:
            translations (List[Dict[str, str]]): List of translation dictionaries
            timestamp (Optional[datetime]): Custom timestamp, defaults to now
            
        Returns:
            bool: True if logged successfully, False otherwise
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
        
        try:
            if self._use_database:
                await self.db_manager.log_bulk_translation(translations, timestamp)
            else:
                # Fallback to in-memory logging
                for translation in translations:
                    log_entry = {
                        "original_text": translation["original_text"],
                        "translated_text": translation["translated_text"],
                        "target_language": translation["target_language"],
                        "timestamp": timestamp.isoformat()
                    }
                    self._in_memory_logs.append(log_entry)
                
                # Keep only last 1000 entries
                if len(self._in_memory_logs) > 1000:
                    self._in_memory_logs = self._in_memory_logs[-1000:]
            
            return True
            
        except Exception as e:
            print(f"Error logging bulk translations: {e}")
            # Try fallback to in-memory if database fails
            if self._use_database:
                try:
                    for translation in translations:
                        log_entry = {
                            "original_text": translation["original_text"],
                            "translated_text": translation["translated_text"],
                            "target_language": translation["target_language"],
                            "timestamp": timestamp.isoformat()
                        }
                        self._in_memory_logs.append(log_entry)
                    
                    self._use_database = False
                    print("Switched to in-memory logging due to database error")
                    return True
                except Exception as fallback_error:
                    print(f"Error in fallback logging: {fallback_error}")
            
            return False
    
    async def get_translation_logs(
        self,
        limit: int = 100,
        offset: int = 0,
        target_language: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve translation logs.
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            target_language (Optional[str]): Filter by target language
            
        Returns:
            List[Dict[str, Any]]: List of translation log records
        """
        try:
            if self._use_database:
                return await self.db_manager.get_translation_logs(
                    limit, offset, target_language
                )
            else:
                # Return from in-memory logs
                logs = self._in_memory_logs.copy()
                
                # Filter by target language if specified
                if target_language:
                    logs = [
                        log for log in logs 
                        if log.get("target_language") == target_language
                    ]
                
                # Sort by timestamp (newest first)
                logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                
                # Apply pagination
                start_idx = offset
                end_idx = offset + limit
                
                return logs[start_idx:end_idx]
                
        except Exception as e:
            print(f"Error retrieving translation logs: {e}")
            return []
    
    async def get_translation_stats(self) -> Dict[str, Any]:
        """
        Get translation statistics.
        
        Returns:
            Dict[str, Any]: Statistics about translations
        """
        try:
            if self._use_database:
                return await self.db_manager.get_translation_stats()
            else:
                # Calculate stats from in-memory logs
                total_translations = len(self._in_memory_logs)
                
                # Count by language
                language_counts = {}
                recent_count = 0
                now = datetime.utcnow()
                
                for log in self._in_memory_logs:
                    lang = log.get("target_language", "unknown")
                    language_counts[lang] = language_counts.get(lang, 0) + 1
                    
                    # Count recent translations (last 24 hours)
                    try:
                        log_time = datetime.fromisoformat(log.get("timestamp", ""))
                        if (now - log_time).total_seconds() < 86400:  # 24 hours
                            recent_count += 1
                    except:
                        pass
                
                return {
                    "total_translations": total_translations,
                    "recent_translations_24h": recent_count,
                    "translations_by_language": [
                        {"language": lang, "count": count}
                        for lang, count in sorted(
                            language_counts.items(), 
                            key=lambda x: x[1], 
                            reverse=True
                        )
                    ]
                }
                
        except Exception as e:
            print(f"Error getting translation stats: {e}")
            return {
                "total_translations": 0,
                "recent_translations_24h": 0,
                "translations_by_language": []
            }
    
    def is_using_database(self) -> bool:
        """
        Check if the logger is using database or in-memory storage.
        
        Returns:
            bool: True if using database, False if using in-memory
        """
        return self._use_database
    
    async def close(self):
        """
        Close the logger and cleanup resources.
        """
        if self.db_manager:
            await self.db_manager.close()


# Global translation logger instance
translation_logger = TranslationLogger()