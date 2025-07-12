from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime

class TranslationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=1000, description="Text to translate")
    target_language: str = Field(..., min_length=2, max_length=5, description="Target language ISO code")
    source_language: Optional[str] = Field(None, min_length=2, max_length=5, description="Source language ISO code")
    
    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError('Text cannot be empty or whitespace only')
        return v.strip()
    
    @validator('target_language', 'source_language')
    def validate_language_codes(cls, v):
        if v:
            return v.lower()
        return v

class BulkTranslationRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=50, description="List of texts to translate")
    target_language: str = Field(..., min_length=2, max_length=5, description="Target language ISO code")
    source_language: Optional[str] = Field(None, min_length=2, max_length=5, description="Source language ISO code")
    
    @validator('texts')
    def validate_texts(cls, v):
        for text in v:
            if not text.strip():
                raise ValueError('Each text must not be empty or whitespace only')
            if len(text) > 1000:
                raise ValueError('Each text must be 1000 characters or less')
        return [text.strip() for text in v]
    
    @validator('target_language', 'source_language')
    def validate_language_codes(cls, v):
        if v:
            return v.lower()
        return v

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    timestamp: datetime
    translation_id: str

class BulkTranslationResponse(BaseModel):
    translations: List[TranslationResponse]
    total_count: int
    timestamp: datetime

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime