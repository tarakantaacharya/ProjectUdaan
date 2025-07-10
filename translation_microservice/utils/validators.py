"""
Input validation utilities for the translation microservice.
Validates text length, language codes, and other input parameters.
"""

from typing import List, Optional
from .constants import SUPPORTED_LANGUAGES, MAX_TEXT_LENGTH


def validate_text(text: str) -> tuple[bool, Optional[str]]:
    """
    Validate input text for translation.
    
    Args:
        text (str): The text to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not text:
        return False, "Text cannot be empty"
    
    if not isinstance(text, str):
        return False, "Text must be a string"
    
    if len(text.strip()) == 0:
        return False, "Text cannot be empty or contain only whitespace"
    
    if len(text) > MAX_TEXT_LENGTH:
        return False, f"Text length cannot exceed {MAX_TEXT_LENGTH} characters"
    
    return True, None


def validate_language_code(language_code: str) -> tuple[bool, Optional[str]]:
    """
    Validate ISO 639-1 language code.
    
    Args:
        language_code (str): The language code to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not language_code:
        return False, "Language code cannot be empty"
    
    if not isinstance(language_code, str):
        return False, "Language code must be a string"
    
    language_code = language_code.lower().strip()
    
    if language_code not in SUPPORTED_LANGUAGES:
        supported_codes = ", ".join(sorted(SUPPORTED_LANGUAGES.keys()))
        return False, f"Unsupported language code '{language_code}'. Supported codes: {supported_codes}"
    
    return True, None


def validate_bulk_texts(texts: List[str]) -> tuple[bool, Optional[str]]:
    """
    Validate a list of texts for bulk translation.
    
    Args:
        texts (List[str]): List of texts to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not texts:
        return False, "Texts list cannot be empty"
    
    if not isinstance(texts, list):
        return False, "Texts must be a list"
    
    if len(texts) == 0:
        return False, "Texts list cannot be empty"
    
    if len(texts) > 100:  # Reasonable limit for bulk operations
        return False, "Cannot process more than 100 texts at once"
    
    for i, text in enumerate(texts):
        is_valid, error_msg = validate_text(text)
        if not is_valid:
            return False, f"Text at index {i}: {error_msg}"
    
    return True, None


def get_supported_languages() -> dict:
    """
    Get the dictionary of supported language codes and names.
    
    Returns:
        dict: Dictionary of supported languages
    """
    return SUPPORTED_LANGUAGES.copy()


def is_language_supported(language_code: str) -> bool:
    """
    Check if a language code is supported.
    
    Args:
        language_code (str): The language code to check
        
    Returns:
        bool: True if supported, False otherwise
    """
    if not language_code or not isinstance(language_code, str):
        return False
    
    return language_code.lower().strip() in SUPPORTED_LANGUAGES