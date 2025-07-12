import sys
import os
import asyncio

# Add the root project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.translation_service import TranslationService
from models.translation_models import TranslationRequest
from services.database_service import init_db
init_db()

def test_translation_service():
    service = TranslationService()
    
    request = TranslationRequest(
        text="hello",
        target_language="ta",
        source_language="en"
    )
    
    result = service.translate_text(request)
    
    assert result.translated_text is not None
    assert result.target_language == "ta"
    assert result.original_text == "hello"

if __name__ == "__main__":
    test_translation_service()
    print("✅ Test passed")

