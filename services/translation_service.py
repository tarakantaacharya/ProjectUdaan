from typing import Dict, List, Optional
import logging
from models.translation_models import TranslationRequest, BulkTranslationRequest, TranslationResponse
from utils.db_logger import log_translation
from utils.lang_helper import detect_language, validate_language_code
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        # Mock translation dictionary - in production, this would use Google Translate API
        self.translations = {
            'en': {
                'ta': {
                    'hello': 'வணக்கம்',
                    'goodbye': 'வரவேற்கிறேன்',
                    'thank you': 'நன்றி',
                    'please': 'தயவுசெய்து',
                    'how are you': 'நீங்கள் எப்படி இருக்கிறீர்கள்',
                    'good morning': 'காலை வணக்கம்',
                    'good night': 'இனிய இரவு',
                    'yes': 'ஆம்',
                    'no': 'இல்லை',
                    'water': 'நீர்',
                    'food': 'உணவு',
                    'love': 'அன்பு',
                    'family': 'குடும்பம்',
                    'friend': 'நண்பன்',
                    'book': 'புத்தகம்'
                },
                'hi': {
                    'hello': 'नमस्ते',
                    'goodbye': 'अलविदा',
                    'thank you': 'धन्यवाद',
                    'please': 'कृपया',
                    'how are you': 'आप कैसे हैं',
                    'good morning': 'सुप्रभात',
                    'good night': 'शुभ रात्रि',
                    'yes': 'हाँ',
                    'no': 'नहीं',
                    'water': 'पानी',
                    'food': 'भोजन',
                    'love': 'प्रेम',
                    'family': 'परिवार',
                    'friend': 'मित्र',
                    'book': 'पुस्तक'
                },
                'kn': {
                    'hello': 'ನಮಸ್ಕಾರ',
                    'goodbye': 'ವಿದಾಯ',
                    'thank you': 'ಧನ್ಯವಾದ',
                    'please': 'ದಯವಿಟ್ಟು',
                    'how are you': 'ನೀವು ಹೇಗಿದ್ದೀರಿ',
                    'good morning': 'ಶುಭೋದಯ',
                    'good night': 'ಶುಭ ರಾತ್ರಿ',
                    'yes': 'ಹೌದು',
                    'no': 'ಇಲ್ಲ',
                    'water': 'ನೀರು',
                    'food': 'ಆಹಾರ',
                    'love': 'ಪ್ರೀತಿ',
                    'family': 'ಕುಟುಂಬ',
                    'friend': 'ಸ್ನೇಹಿತ',
                    'book': 'ಪುಸ್ತಕ'
                },
                'bn': {
                    'hello': 'হ্যালো',
                    'goodbye': 'বিদায়',
                    'thank you': 'ধন্যবাদ',
                    'please': 'দয়া করে',
                    'how are you': 'আপনি কেমন আছেন',
                    'good morning': 'সুপ্রভাত',
                    'good night': 'শুভ রাত্রি',
                    'yes': 'হ্যাঁ',
                    'no': 'না',
                    'water': 'পানি',
                    'food': 'খাবার',
                    'love': 'ভালোবাসা',
                    'family': 'পরিবার',
                    'friend': 'বন্ধু',
                    'book': 'বই'
                }
            }
        }
    
    def translate_text(self, request: TranslationRequest) -> TranslationResponse:
        """Translate a single text"""
        try:
            # Validate target language
            if not validate_language_code(request.target_language):
                raise ValueError(f"Unsupported target language: {request.target_language}")
            
            # Detect source language if not provided
            source_lang = request.source_language or detect_language(request.text)
            
            # Perform translation
            translated_text = self._perform_translation(
                request.text, source_lang, request.target_language
            )
            
            # Create response
            translation_id = str(uuid.uuid4())
            timestamp = datetime.now()
            
            response = TranslationResponse(
                original_text=request.text,
                translated_text=translated_text,
                source_language=source_lang,
                target_language=request.target_language,
                timestamp=timestamp,
                translation_id=translation_id
            )
            
            # Log translation
            log_translation(
                translation_id=translation_id,
                original_text=request.text,
                translated_text=translated_text,
                source_language=source_lang,
                target_language=request.target_language,
                timestamp=timestamp
            )
            
            logger.info(f"Translation completed: {translation_id}")
            return response
            
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            raise
    
    def translate_bulk(self, request: BulkTranslationRequest) -> Dict:
        """Translate multiple texts"""
        try:
            translations = []
            timestamp = datetime.now()
            
            for text in request.texts:
                single_request = TranslationRequest(
                    text=text,
                    target_language=request.target_language,
                    source_language=request.source_language
                )
                translation = self.translate_text(single_request)
                translations.append(translation)
            
            return {
                "translations": translations,
                "total_count": len(translations),
                "timestamp": timestamp
            }
            
        except Exception as e:
            logger.error(f"Bulk translation failed: {str(e)}")
            raise
    
    def _perform_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """Perform the actual translation using mock dictionary"""
        # Normalize input
        lower_text = text.lower().strip()
        clean_text = ''.join(c for c in lower_text if c.isalnum() or c.isspace())
        translations = self.translations.get(source_lang, {}).get(target_lang, {})

        # ✅ Step 1: Try full cleaned phrase
        if clean_text in translations:
            return translations[clean_text]

        # ✅ Step 2: Word-by-word fallback
        words = clean_text.split()
        translated_words = [
            translations.get(word, word)
            for word in words
        ]
        translated_text = ' '.join(translated_words)

        # ✅ Step 3: If translation is identical to input, return mock
        if translated_text == clean_text:
            return f"[Mock translation to {target_lang}] {text}"

        return translated_text


