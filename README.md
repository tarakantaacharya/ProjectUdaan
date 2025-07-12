# Translation Microservice

A lightweight, modular translation service built with FastAPI.

## Features

- RESTful API for text translation
- Support for multiple languages (Tamil, Hindi, Kannada, Bengali)
- Bulk translation support
- Request logging with SQLite database
- Health check endpoint
- Input validation and error handling
- Modular architecture
- Docker support

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the service:
   ```bash
   python main.py
   ```

## API Endpoints

### Translation
- `POST /api/v1/translate` - Translate single text
- `POST /api/v1/translate/bulk` - Translate multiple texts
- `GET /api/v1/translate/history` - Get translation history

### Health
- `GET /api/v1/health` - Health check

## Usage Examples

### Single Translation
```bash
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "target_language": "ta"
  }'
```

### Bulk Translation
```bash
curl -X POST "http://localhost:8000/api/v1/translate/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": ["Hello", "Goodbye", "Thank you"],
    "target_language": "hi"
  }'
```

## Docker Deployment

```bash
docker-compose up -d
```

## Architecture

- `main.py` - FastAPI application entry point
- `models/` - Pydantic models for request/response
- `services/` - Business logic and database operations
- `routes/` - API endpoint definitions
- `utils/` - Utility functions
- `config/` - Configuration settings

## Production Considerations

1. Replace mock translation with Google Translate API
2. Use proper database (PostgreSQL/MySQL) instead of SQLite
3. Add authentication and rate limiting
4. Implement proper logging and monitoring
5. Add comprehensive testing
6. Set up CI/CD pipeline
"""
