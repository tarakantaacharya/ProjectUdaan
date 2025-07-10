"""
Translation service that handles both Google Translate API and mock translations.
Provides fallback mechanism when Google API is not available or fails.
"""

import os
import asyncio
from typing import List, Optional, Dict, Any
from googletrans import Translator
import re

from ..utils.constants import MOCK_TRANSLATIONS, SUPPORTED_LANGUAGES
from ..utils.validators import validate_text, validate_language_code


class TranslationService:
    """
    Service for handling text translation using Google Translate API or mock fallback.
    """
    
    def __init__(self):
        """Initialize the translation service."""
        self.google_translator = None
        self.use_google_api = False
        self._initialize_google_translator()
    
    def _initialize_google_translator(self):
        """
        Initialize Google Translator if API key is available.
        Note: googletrans library doesn't require API key but may have rate limits.
        """
        try:
            # Check if we should use Google API (can be controlled via environment)
            use_google = os.getenv('USE_GOOGLE_TRANSLATE', 'true').lower() == 'true'
            
            if use_google:
                self.google_translator = Translator()
                self.use_google_api = True
                print("Google Translate API initialized successfully")
            else:
                print("Google Translate API disabled via environment variable")
                
        except Exception as e:
            print(f"Failed to initialize Google Translate API: {e}")
            print("Falling back to mock translations")
            self.use_google_api = False
    
    async def translate_text(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate a single text to the target language.
        
        Args:
            text (str): The text to translate
            target_language (str): The target language code (ISO 639-1)
            
        Returns:
            Dict[str, Any]: Translation result with original_text, translated_text, 
                           target_language, and translation_method
        """
        # Validate inputs
        text_valid, text_error = validate_text(text)
        if not text_valid:
            raise ValueError(f"Invalid text: {text_error}")
        
        lang_valid, lang_error = validate_language_code(target_language)
        if not lang_valid:
            raise ValueError(f"Invalid language code: {lang_error}")
        
        target_language = target_language.lower().strip()
        
        # Try Google Translate first if available
        if self.use_google_api and self.google_translator:
            try:
                translated_text = await self._translate_with_google(text, target_language)
                return {
                    "original_text": text,
                    "translated_text": translated_text,
                    "target_language": target_language,
                    "translation_method": "google_api"
                }
            except Exception as e:
                print(f"Google Translate failed: {e}")
                print("Falling back to mock translation")
        
        # Fallback to mock translation
        translated_text = self._translate_with_mock(text, target_language)
        return {
            "original_text": text,
            "translated_text": translated_text,
            "target_language": target_language,
            "translation_method": "mock"
        }
    
    async def translate_bulk(
        self, 
        texts: List[str], 
        target_language: str
    ) -> List[Dict[str, Any]]:
        """
        Translate multiple texts to the target language.
        
        Args:
            texts (List[str]): List of texts to translate
            target_language (str): The target language code (ISO 639-1)
            
        Returns:
            List[Dict[str, Any]]: List of translation results
        """
        # Validate target language once
        lang_valid, lang_error = validate_language_code(target_language)
        if not lang_valid:
            raise ValueError(f"Invalid language code: {lang_error}")
        
        target_language = target_language.lower().strip()
        
        # Translate each text
        results = []
        for text in texts:
            try:
                result = await self.translate_text(text, target_language)
                results.append(result)
            except Exception as e:
                # Include error information in the result
                results.append({
                    "original_text": text,
                    "translated_text": f"Translation failed: {str(e)}",
                    "target_language": target_language,
                    "translation_method": "error",
                    "error": str(e)
                })
        
        return results
    
    async def _translate_with_google(self, text: str, target_language: str) -> str:
        """
        Translate text using Google Translate API.
        
        Args:
            text (str): The text to translate
            target_language (str): The target language code
            
        Returns:
            str: The translated text
        """
        try:
            # Run the translation in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, 
                lambda: self.google_translator.translate(text, dest=target_language)
            )
            
            if result and result.text:
                return result.text
            else:
                raise Exception("Google Translate returned empty result")
                
        except Exception as e:
            raise Exception(f"Google Translate API error: {str(e)}")
    
    def _translate_with_mock(self, text: str, target_language: str) -> str:
        """
        Translate text using mock dictionary.
        
        Args:
            text (str): The text to translate
            target_language (str): The target language code
            
        Returns:
            str: The translated text (or original if no translation found)
        """
        # Convert text to lowercase for matching
        text_lower = text.lower().strip()
        
        # Check if we have a direct translation
        if text_lower in MOCK_TRANSLATIONS:
            if target_language in MOCK_TRANSLATIONS[text_lower]:
                return MOCK_TRANSLATIONS[text_lower][target_language]
        
        # Try to find partial matches for common phrases
        for phrase, translations in MOCK_TRANSLATIONS.items():
            if phrase in text_lower or text_lower in phrase:
                if target_language in translations:
                    # Replace the matched phrase with translation
                    translated_phrase = translations[target_language]
                    return text_lower.replace(phrase, translated_phrase)
        
        # If no translation found, return a formatted response
        language_name = SUPPORTED_LANGUAGES.get(target_language, target_language)
        return f"[Mock Translation to {language_name}] {text}"
    
    def get_supported_languages(self) -> Dict[str, str]:
        """
        Get the list of supported languages.
        
        Returns:
            Dict[str, str]: Dictionary of language codes and names
        """
        return SUPPORTED_LANGUAGES.copy()
    
    def is_using_google_api(self) -> bool:
        """
        Check if the service is using Google API.
        
        Returns:
            bool: True if using Google API, False if using mock
        """
        return self.use_google_api
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the translation service.
        
        Returns:
            Dict[str, Any]: Health check results
        """
        health_info = {
            "service": "translation",
            "status": "healthy",
            "translation_method": "google_api" if self.use_google_api else "mock",
            "supported_languages_count": len(SUPPORTED_LANGUAGES)
        }
        
        # Test translation capability
        try:
            test_result = await self.translate_text("hello", "hi")
            health_info["test_translation"] = {
                "success": True,
                "method_used": test_result.get("translation_method")
            }
        except Exception as e:
            health_info["test_translation"] = {
                "success": False,
                "error": str(e)
            }
            health_info["status"] = "degraded"
        
        return health_info


# Global translation service instance
translation_service = TranslationService()