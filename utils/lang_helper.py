import re
from typing import Optional

# Supported language codes
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ta': 'Tamil',
    'hi': 'Hindi',
    'kn': 'Kannada',
    'bn': 'Bengali'
}

def detect_language(text: str) -> str:
    """Simple language detection - in production, use proper language detection library"""
    import re
    if re.search(r'[\u0B80-\u0BFF]', text):  # Tamil range
        return 'ta'
    elif re.search(r'[\u0900-\u097F]', text):  # Hindi range
        return 'hi'
    elif re.search(r'[\u0C80-\u0CFF]', text):  # Kannada range
        return 'kn'
    elif re.search(r'[\u0980-\u09FF]', text):  # Bengali range
        return 'bn'
    else:
        return 'en'

def validate_language_code(lang_code: str) -> bool:
    """Validate if language code is supported"""
    return lang_code.lower() in SUPPORTED_LANGUAGES

def get_supported_languages():
    """Get list of supported languages"""
    return SUPPORTED_LANGUAGES
