from fastapi import APIRouter, HTTPException, Depends
from models.translation_models import (
    TranslationRequest, BulkTranslationRequest, 
    TranslationResponse, BulkTranslationResponse,  # ← add this
    ErrorResponse
)
from services.translation_service import TranslationService
from services.database_service import get_translation_history
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()  # Make sure this line exists and is not commented out

def get_translation_service():
    return TranslationService()

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(
    request: TranslationRequest,
    service: TranslationService = Depends(get_translation_service)
):
    """Translate a single text"""
    try:
        result = service.translate_text(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/translate/bulk", response_model=BulkTranslationResponse)
async def translate_bulk(
    request: BulkTranslationRequest,
    service: TranslationService = Depends(get_translation_service)
):
    """Translate multiple texts"""
    try:
        result = service.translate_bulk(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Bulk translation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/translate/history")
async def get_history(limit: int = 100):
    """Get translation history"""
    try:
        history = get_translation_history(limit)
        return {
            "history": history,
            "count": len(history),
            "timestamp": datetime.now()
        }
    except Exception as e:
        logger.error(f"History retrieval error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")