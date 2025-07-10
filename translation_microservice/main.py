"""
Main entry point for the Translation Microservice.
FastAPI application with translation endpoints, health checks, and proper error handling.

Project Udaan - IIT Bombay
Translation Microservice v1.0.0
"""

import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from translation_microservice.routes import translate, health
from translation_microservice.services.logger import translation_logger
from translation_microservice.services.translator import translation_service

# Load environment variables
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events.
    """
    # Startup
    print("🚀 Starting Translation Microservice...")
    
    # Initialize services
    await translation_logger.initialize()
    print("✅ Translation logger initialized")
    
    # Perform health check on translation service
    health_result = await translation_service.health_check()
    if health_result.get("status") == "healthy":
        print("✅ Translation service is healthy")
    else:
        print("⚠️  Translation service is degraded")
    
    print("🎯 Translation Microservice is ready!")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Translation Microservice...")
    await translation_logger.close()
    print("✅ Services closed gracefully")


# Create FastAPI application
app = FastAPI(
    title="Translation Microservice",
    description="""
    🚀 **Translation Microservice for Project Udaan - IIT Bombay**
    
    A production-grade RESTful API for text translation supporting multiple languages.
    
    ## Features
    
    * **Single Translation**: Translate individual texts up to 1000 characters
    * **Bulk Translation**: Translate multiple texts in a single request
    * **Multi-language Support**: Support for 20+ languages including Indian languages
    * **Dual Translation Methods**: Google Translate API with mock fallback
    * **Request Logging**: Complete audit trail of all translation requests
    * **Input Validation**: Comprehensive validation with structured error responses
    * **Health Monitoring**: Health check endpoints for service monitoring
    
    ## Supported Languages
    
    Hindi (hi), Tamil (ta), Kannada (kn), Bengali (bn), Telugu (te), Malayalam (ml),
    Gujarati (gu), Marathi (mr), Punjabi (pa), Odia (or), Assamese (as), Urdu (ur),
    English (en), Spanish (es), French (fr), German (de), Italian (it), Portuguese (pt),
    Russian (ru), Japanese (ja), Korean (ko), Chinese (zh), Arabic (ar)
    
    ## Translation Methods
    
    * **Google API**: Uses Google Translate API when available
    * **Mock Translation**: Dictionary-based fallback for common phrases
    
    ## Error Handling
    
    All endpoints return structured JSON errors with appropriate HTTP status codes:
    * `422` - Validation errors (invalid input)
    * `500` - Internal server errors
    """,
    version="1.0.0",
    contact={
        "name": "Project Udaan - IIT Bombay",
        "email": "support@projectudaan.iitb.ac.in"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(translate.router, prefix="/api/v1")
app.include_router(health.router, prefix="/api/v1")


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "type": "internal_error",
            "path": str(request.url.path)
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with service information.
    """
    return {
        "service": "Translation Microservice",
        "version": "1.0.0",
        "project": "Project Udaan - IIT Bombay",
        "status": "running",
        "endpoints": {
            "translate": "/api/v1/translate",
            "bulk_translate": "/api/v1/translate/bulk",
            "health": "/api/v1/health",
            "supported_languages": "/api/v1/translate/languages",
            "translation_logs": "/api/v1/translate/logs",
            "translation_stats": "/api/v1/translate/stats",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "documentation": "/docs"
    }


# Additional utility endpoints
@app.get("/api/v1/info", tags=["Info"])
async def service_info():
    """
    Get detailed service information.
    """
    return {
        "service": "Translation Microservice",
        "version": "1.0.0",
        "project": "Project Udaan - IIT Bombay",
        "description": "Production-grade RESTful Translation API",
        "features": {
            "single_translation": True,
            "bulk_translation": True,
            "request_logging": True,
            "input_validation": True,
            "error_handling": True,
            "health_monitoring": True,
            "multi_language_support": True
        },
        "translation_methods": {
            "google_api": translation_service.is_using_google_api(),
            "mock_fallback": True
        },
        "supported_languages_count": len(translation_service.get_supported_languages()),
        "max_text_length": 1000,
        "max_bulk_size": 100
    }


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment variables
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 9000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"🚀 Starting server on {host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 ReDoc Documentation: http://{host}:{port}/redoc")
    
    uvicorn.run(
        "translation_microservice.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )