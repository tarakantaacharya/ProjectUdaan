"""
Translation endpoints for the microservice.
Handles single and bulk translation requests with proper validation and logging.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime

from ..services.translator import translation_service
from ..services.logger import translation_logger
from ..utils.validators import validate_text, validate_language_code, validate_bulk_texts

# Create router for translation endpoints
router = APIRouter(tags=["Translation"])


# Pydantic models for request/response validation
class TranslationRequest(BaseModel):
    """Request model for single translation."""
    text: str = Field(..., description="Text to translate (max 1000 characters)")
    target_language: str = Field(..., description="Target language code (ISO 639-1)")
    
    @validator('text')
    def validate_text_field(cls, v):
        is_valid, error_msg = validate_text(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @validator('target_language')
    def validate_language_field(cls, v):
        is_valid, error_msg = validate_language_code(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v.lower().strip()


class BulkTranslationRequest(BaseModel):
    """Request model for bulk translation."""
    texts: List[str] = Field(..., description="List of texts to translate")
    target_language: str = Field(..., description="Target language code (ISO 639-1)")
    
    @validator('texts')
    def validate_texts_field(cls, v):
        is_valid, error_msg = validate_bulk_texts(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v
    
    @validator('target_language')
    def validate_language_field(cls, v):
        is_valid, error_msg = validate_language_code(v)
        if not is_valid:
            raise ValueError(error_msg)
        return v.lower().strip()


class TranslationResponse(BaseModel):
    """Response model for single translation."""
    original_text: str
    translated_text: str
    target_language: str
    translation_method: Optional[str] = None
    timestamp: Optional[str] = None


class BulkTranslationResponse(BaseModel):
    """Response model for bulk translation."""
    translations: List[TranslationResponse]
    total_count: int
    successful_count: int
    failed_count: int
    target_language: str


@router.post("/translate", response_model=TranslationResponse, status_code=status.HTTP_200_OK)
async def translate_text(request: TranslationRequest):
    """
    Translate a single text to the target language.
    
    Args:
        request (TranslationRequest): Translation request containing text and target language
        
    Returns:
        TranslationResponse: Translation result
        
    Raises:
        HTTPException: For validation errors or translation failures
    """
    try:
        # Perform translation
        result = await translation_service.translate_text(
            request.text, 
            request.target_language
        )
        
        # Log the translation request
        timestamp = datetime.utcnow()
        await translation_logger.log_single_translation(
            original_text=result["original_text"],
            translated_text=result["translated_text"],
            target_language=result["target_language"],
            timestamp=timestamp
        )
        
        # Prepare response
        response = TranslationResponse(
            original_text=result["original_text"],
            translated_text=result["translated_text"],
            target_language=result["target_language"],
            translation_method=result.get("translation_method"),
            timestamp=timestamp.isoformat()
        )
        
        return response
        
    except ValueError as e:
        # Validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Validation Error",
                "message": str(e),
                "type": "validation_error"
            }
        )
    except Exception as e:
        # Internal server errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Translation Error",
                "message": "Failed to translate text",
                "details": str(e),
                "type": "translation_error"
            }
        )


@router.post("/translate/bulk", response_model=BulkTranslationResponse, status_code=status.HTTP_200_OK)
async def translate_bulk(request: BulkTranslationRequest):
    """
    Translate multiple texts to the target language.
    
    Args:
        request (BulkTranslationRequest): Bulk translation request
        
    Returns:
        BulkTranslationResponse: Bulk translation results
        
    Raises:
        HTTPException: For validation errors or translation failures
    """
    try:
        # Perform bulk translation
        results = await translation_service.translate_bulk(
            request.texts, 
            request.target_language
        )
        
        # Prepare translations for logging and response
        translations = []
        successful_translations = []
        successful_count = 0
        failed_count = 0
        timestamp = datetime.utcnow()
        
        for result in results:
            translation_response = TranslationResponse(
                original_text=result["original_text"],
                translated_text=result["translated_text"],
                target_language=result["target_language"],
                translation_method=result.get("translation_method"),
                timestamp=timestamp.isoformat()
            )
            translations.append(translation_response)
            
            # Count successful vs failed translations
            if result.get("translation_method") != "error":
                successful_count += 1
                successful_translations.append({
                    "original_text": result["original_text"],
                    "translated_text": result["translated_text"],
                    "target_language": result["target_language"]
                })
            else:
                failed_count += 1
        
        # Log successful translations
        if successful_translations:
            await translation_logger.log_bulk_translation(
                successful_translations, 
                timestamp
            )
        
        # Prepare response
        response = BulkTranslationResponse(
            translations=translations,
            total_count=len(translations),
            successful_count=successful_count,
            failed_count=failed_count,
            target_language=request.target_language
        )
        
        return response
        
    except ValueError as e:
        # Validation errors
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "Validation Error",
                "message": str(e),
                "type": "validation_error"
            }
        )
    except Exception as e:
        # Internal server errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Bulk Translation Error",
                "message": "Failed to translate texts",
                "details": str(e),
                "type": "bulk_translation_error"
            }
        )


@router.get("/translate/languages", response_model=Dict[str, str])
async def get_supported_languages():
    """
    Get the list of supported languages.
    
    Returns:
        Dict[str, str]: Dictionary of language codes and names
    """
    try:
        return translation_service.get_supported_languages()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Service Error",
                "message": "Failed to retrieve supported languages",
                "details": str(e)
            }
        )


@router.get("/translate/logs", response_model=List[Dict[str, Any]])
async def get_translation_logs(
    limit: int = 50,
    offset: int = 0,
    target_language: Optional[str] = None
):
    """
    Get translation logs with optional filtering.
    
    Args:
        limit (int): Maximum number of records to return (default: 50)
        offset (int): Number of records to skip (default: 0)
        target_language (Optional[str]): Filter by target language
        
    Returns:
        List[Dict[str, Any]]: List of translation log records
    """
    try:
        # Validate limit and offset
        if limit < 1 or limit > 1000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Limit must be between 1 and 1000"
            )
        
        if offset < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Offset must be non-negative"
            )
        
        # Validate target_language if provided
        if target_language:
            is_valid, error_msg = validate_language_code(target_language)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Invalid language code: {error_msg}"
                )
            target_language = target_language.lower().strip()
        
        # Get logs
        logs = await translation_logger.get_translation_logs(
            limit=limit,
            offset=offset,
            target_language=target_language
        )
        
        return logs
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Service Error",
                "message": "Failed to retrieve translation logs",
                "details": str(e)
            }
        )


@router.get("/translate/stats", response_model=Dict[str, Any])
async def get_translation_stats():
    """
    Get translation statistics.
    
    Returns:
        Dict[str, Any]: Translation statistics
    """
    try:
        stats = await translation_logger.get_translation_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "Service Error",
                "message": "Failed to retrieve translation statistics",
                "details": str(e)
            }
        )