"""
Health check endpoint for the translation microservice.
Provides system health status and service availability information.
"""

from fastapi import APIRouter
from typing import Dict, Any

from ..services.translator import translation_service
from ..services.logger import translation_logger

# Create router for health endpoints
router = APIRouter(tags=["Health"])


@router.get("/health", response_model=Dict[str, Any])
async def health_check():
    """
    Health check endpoint that returns the service status.
    
    Returns:
        Dict[str, Any]: Health status information
    """
    try:
        # Get translation service health
        translation_health = await translation_service.health_check()
        
        # Check logger status
        logger_status = {
            "service": "logger",
            "status": "healthy",
            "storage_method": "database" if translation_logger.is_using_database() else "in_memory"
        }
        
        # Overall health status
        overall_status = "ok"
        if translation_health.get("status") != "healthy":
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "timestamp": translation_health.get("timestamp"),
            "services": {
                "translation": translation_health,
                "logger": logger_status
            },
            "version": "1.0.0",
            "environment": "production"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "services": {
                "translation": {"status": "error", "error": str(e)},
                "logger": {"status": "unknown"}
            }
        }


@router.get("/health/detailed", response_model=Dict[str, Any])
async def detailed_health_check():
    """
    Detailed health check endpoint with comprehensive system information.
    
    Returns:
        Dict[str, Any]: Detailed health status and statistics
    """
    try:
        # Get translation service health
        translation_health = await translation_service.health_check()
        
        # Get translation statistics
        translation_stats = await translation_logger.get_translation_stats()
        
        # Logger health with stats
        logger_status = {
            "service": "logger",
            "status": "healthy",
            "storage_method": "database" if translation_logger.is_using_database() else "in_memory",
            "statistics": translation_stats
        }
        
        # System information
        system_info = {
            "supported_languages": translation_service.get_supported_languages(),
            "translation_method": "google_api" if translation_service.is_using_google_api() else "mock",
            "features": {
                "single_translation": True,
                "bulk_translation": True,
                "request_logging": True,
                "input_validation": True,
                "error_handling": True
            }
        }
        
        # Overall health status
        overall_status = "ok"
        if translation_health.get("status") != "healthy":
            overall_status = "degraded"
        
        return {
            "status": overall_status,
            "services": {
                "translation": translation_health,
                "logger": logger_status
            },
            "system": system_info,
            "version": "1.0.0",
            "environment": "production"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "services": {
                "translation": {"status": "error", "error": str(e)},
                "logger": {"status": "unknown"}
            }
        }