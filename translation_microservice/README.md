# 🚀 Translation Microservice

A production-grade RESTful Translation API built with FastAPI for **Project Udaan - IIT Bombay**.

## 🎯 Features

- **Single & Bulk Translation**: Translate individual texts or multiple texts in one request
- **Multi-language Support**: 20+ languages including Indian languages (Hindi, Tamil, Kannada, Bengali, etc.)
- **Dual Translation Methods**: Google Translate API with intelligent mock fallback
- **Request Logging**: Complete audit trail stored in SQLite database
- **Input Validation**: Comprehensive validation with structured error responses
- **Health Monitoring**: Detailed health check endpoints for service monitoring
- **Production Ready**: Docker support, proper error handling, and extensive documentation

## 🏗️ Architecture

```
translation_microservice/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── Dockerfile             # Container configuration
├── routes/                # API route handlers
│   ├── translate.py       # Translation endpoints
│   └── health.py          # Health check endpoints
├── services/              # Business logic services
│   ├── translator.py      # Translation service (Google API + Mock)
│   └── logger.py          # Request logging service
├── utils/                 # Utility functions
│   ├── validators.py      # Input validation
│   └── constants.py       # Language codes and mock translations
├── db/                    # Database operations
│   └── database.py        # SQLite database manager
├── test/                  # Unit tests
│   └── test_translate.py  # API and service tests
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd translation_microservice
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env file as needed
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at:
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker Deployment

### Build and run with Docker

```bash
# Build the image
docker build -t translation-microservice .

# Run the container
docker run -p 8000:8000 translation-microservice
```

### Using Docker Compose (optional)

```yaml
version: '3.8'
services:
  translation-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - USE_GOOGLE_TRANSLATE=true
      - DEBUG=false
    volumes:
      - ./data:/app/data
```

## 📚 API Documentation

### Core Endpoints

#### 1. Single Translation
```http
POST /api/v1/translate
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "target_language": "hi"
}
```

**Response:**
```json
{
  "original_text": "Hello, how are you?",
  "translated_text": "नमस्ते, आप कैसे हैं?",
  "target_language": "hi",
  "translation_method": "google_api",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### 2. Bulk Translation
```http
POST /api/v1/translate/bulk
Content-Type: application/json

{
  "texts": ["Hello", "Good morning", "Thank you"],
  "target_language": "hi"
}
```

**Response:**
```json
{
  "translations": [
    {
      "original_text": "Hello",
      "translated_text": "नमस्ते",
      "target_language": "hi",
      "translation_method": "google_api",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "total_count": 3,
  "successful_count": 3,
  "failed_count": 0,
  "target_language": "hi"
}
```

#### 3. Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "ok",
  "services": {
    "translation": {
      "status": "healthy",
      "translation_method": "google_api"
    },
    "logger": {
      "status": "healthy",
      "storage_method": "database"
    }
  }
}
```

### Additional Endpoints

- `GET /api/v1/translate/languages` - Get supported languages
- `GET /api/v1/translate/logs` - Get translation logs
- `GET /api/v1/translate/stats` - Get translation statistics
- `GET /api/v1/health/detailed` - Detailed health information
- `GET /api/v1/info` - Service information

## 🌍 Supported Languages

| Code | Language | Code | Language |
|------|----------|------|----------|
| hi   | Hindi    | en   | English  |
| ta   | Tamil    | es   | Spanish  |
| kn   | Kannada  | fr   | French   |
| bn   | Bengali  | de   | German   |
| te   | Telugu   | it   | Italian  |
| ml   | Malayalam| pt   | Portuguese|
| gu   | Gujarati | ru   | Russian  |
| mr   | Marathi  | ja   | Japanese |
| pa   | Punjabi  | ko   | Korean   |
| or   | Odia     | zh   | Chinese  |
| as   | Assamese | ar   | Arabic   |
| ur   | Urdu     |      |          |

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Translation Service
USE_GOOGLE_TRANSLATE=true

# Database
DATABASE_PATH=translation_logs.db
```

### Translation Methods

#### Google Translate API
- **Pros**: High accuracy, supports many languages
- **Cons**: Requires internet, may have rate limits
- **Usage**: Set `USE_GOOGLE_TRANSLATE=true`

#### Mock Translation
- **Pros**: Works offline, fast response
- **Cons**: Limited vocabulary, basic translations
- **Usage**: Automatic fallback when Google API fails

## 🧪 Testing

### Run Unit Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest test/ -v

# Run with coverage
pytest test/ --cov=. --cov-report=html
```

### Manual Testing with cURL

```bash
# Single translation
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "target_language": "hi"}'

# Bulk translation
curl -X POST "http://localhost:8000/api/v1/translate/bulk" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Hello", "Goodbye"], "target_language": "hi"}'

# Health check
curl "http://localhost:8000/api/v1/health"

# Get supported languages
curl "http://localhost:8000/api/v1/translate/languages"
```

## 📊 Monitoring & Logging

### Request Logging
All translation requests are automatically logged with:
- Original text
- Translated text
- Target language
- Timestamp
- Translation method used

### Health Monitoring
- `/api/v1/health` - Basic health status
- `/api/v1/health/detailed` - Comprehensive health information
- `/api/v1/translate/stats` - Translation statistics

### Database
- SQLite database for persistent logging
- Automatic fallback to in-memory storage
- Database initialization on startup

## 🔒 Security Considerations

- Input validation for all endpoints
- SQL injection prevention
- Rate limiting (configurable)
- CORS configuration
- Non-root Docker user
- Structured error responses (no sensitive data exposure)

## 🚨 Error Handling

### Validation Errors (422)
```json
{
  "detail": {
    "error": "Validation Error",
    "message": "Text length cannot exceed 1000 characters",
    "type": "validation_error"
  }
}
```

### Translation Errors (500)
```json
{
  "detail": {
    "error": "Translation Error",
    "message": "Failed to translate text",
    "type": "translation_error"
  }
}
```

## 🔄 API Versioning

Current version: `v1`
- All endpoints are prefixed with `/api/v1/`
- Backward compatibility maintained
- Version information available at `/api/v1/info`

## 📈 Performance

- **Single Translation**: ~100-500ms (depending on method)
- **Bulk Translation**: Parallel processing for better performance
- **Database Operations**: Optimized with indexes
- **Memory Usage**: Efficient with connection pooling

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- **Project**: Project Udaan - IIT Bombay
- **Email**: support@projectudaan.iitb.ac.in
- **Documentation**: http://localhost:8000/docs

## 🎉 Acknowledgments

- **FastAPI** - Modern, fast web framework
- **Google Translate** - Translation API service
- **SQLite** - Lightweight database
- **Project Udaan - IIT Bombay** - Project sponsorship

---

**Built with ❤️ for Project Udaan - IIT Bombay**