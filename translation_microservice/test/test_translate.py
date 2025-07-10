"""
Unit tests for the translation microservice.
Tests translation endpoints, validation, and error handling.
"""

import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Import the FastAPI app
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


class TestTranslationAPI:
    """Test class for translation API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create a test client."""
        return TestClient(app)
    
    @pytest.fixture
    async def async_client(self):
        """Create an async test client."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Translation Microservice"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] in ["ok", "degraded", "error"]
    
    def test_supported_languages_endpoint(self, client):
        """Test the supported languages endpoint."""
        response = client.get("/api/v1/translate/languages")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "hi" in data  # Hindi should be supported
        assert "en" in data  # English should be supported
    
    def test_single_translation_valid(self, client):
        """Test single translation with valid input."""
        payload = {
            "text": "hello",
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["original_text"] == "hello"
        assert data["target_language"] == "hi"
        assert "translated_text" in data
        assert "translation_method" in data
    
    def test_single_translation_empty_text(self, client):
        """Test single translation with empty text."""
        payload = {
            "text": "",
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error" in data["detail"]
    
    def test_single_translation_long_text(self, client):
        """Test single translation with text exceeding limit."""
        payload = {
            "text": "a" * 1001,  # Exceeds 1000 character limit
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error" in data["detail"]
    
    def test_single_translation_invalid_language(self, client):
        """Test single translation with invalid language code."""
        payload = {
            "text": "hello",
            "target_language": "invalid"
        }
        response = client.post("/api/v1/translate", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error" in data["detail"]
    
    def test_bulk_translation_valid(self, client):
        """Test bulk translation with valid input."""
        payload = {
            "texts": ["hello", "good morning", "thank you"],
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate/bulk", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["total_count"] == 3
        assert data["target_language"] == "hi"
        assert len(data["translations"]) == 3
        assert data["successful_count"] >= 0
        assert data["failed_count"] >= 0
    
    def test_bulk_translation_empty_list(self, client):
        """Test bulk translation with empty text list."""
        payload = {
            "texts": [],
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate/bulk", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error" in data["detail"]
    
    def test_bulk_translation_too_many_texts(self, client):
        """Test bulk translation with too many texts."""
        payload = {
            "texts": ["hello"] * 101,  # Exceeds limit
            "target_language": "hi"
        }
        response = client.post("/api/v1/translate/bulk", json=payload)
        assert response.status_code == 422
        data = response.json()
        assert "error" in data["detail"]
    
    def test_translation_logs_endpoint(self, client):
        """Test translation logs endpoint."""
        # First, make a translation to ensure there's data
        payload = {
            "text": "test",
            "target_language": "hi"
        }
        client.post("/api/v1/translate", json=payload)
        
        # Then get logs
        response = client.get("/api/v1/translate/logs?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_translation_stats_endpoint(self, client):
        """Test translation statistics endpoint."""
        response = client.get("/api/v1/translate/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_translations" in data
        assert "recent_translations_24h" in data
        assert "translations_by_language" in data
    
    def test_service_info_endpoint(self, client):
        """Test service info endpoint."""
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Translation Microservice"
        assert "features" in data
        assert "translation_methods" in data
    
    def test_detailed_health_endpoint(self, client):
        """Test detailed health check endpoint."""
        response = client.get("/api/v1/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "services" in data
        assert "system" in data


class TestValidationFunctions:
    """Test class for validation utility functions."""
    
    def test_text_validation(self):
        """Test text validation function."""
        from utils.validators import validate_text
        
        # Valid text
        is_valid, error = validate_text("hello world")
        assert is_valid is True
        assert error is None
        
        # Empty text
        is_valid, error = validate_text("")
        assert is_valid is False
        assert "empty" in error.lower()
        
        # Text too long
        is_valid, error = validate_text("a" * 1001)
        assert is_valid is False
        assert "1000" in error
    
    def test_language_validation(self):
        """Test language code validation function."""
        from utils.validators import validate_language_code
        
        # Valid language code
        is_valid, error = validate_language_code("hi")
        assert is_valid is True
        assert error is None
        
        # Invalid language code
        is_valid, error = validate_language_code("invalid")
        assert is_valid is False
        assert "Unsupported" in error
        
        # Empty language code
        is_valid, error = validate_language_code("")
        assert is_valid is False
        assert "empty" in error.lower()


class TestTranslationService:
    """Test class for translation service functionality."""
    
    @pytest.mark.asyncio
    async def test_translation_service_health(self):
        """Test translation service health check."""
        from services.translator import translation_service
        
        health = await translation_service.health_check()
        assert "service" in health
        assert "status" in health
        assert health["service"] == "translation"
    
    @pytest.mark.asyncio
    async def test_mock_translation(self):
        """Test mock translation functionality."""
        from services.translator import translation_service
        
        # Test with a known phrase
        result = await translation_service.translate_text("hello", "hi")
        assert result["original_text"] == "hello"
        assert result["target_language"] == "hi"
        assert "translated_text" in result
        assert "translation_method" in result


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])