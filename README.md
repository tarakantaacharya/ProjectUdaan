# 🌍 Translation Microservice

```markdown
A lightweight, modular translation service built with **FastAPI** that supports multi-language translation and is ready for production extension.

---

## 🚀 Features

- ✅ RESTful API for single and bulk text translation
- 🌐 Supports multiple languages: Tamil (`ta`), Hindi (`hi`), Kannada (`kn`), Bengali (`bn`)
- 🗂️ SQLite-based request logging
- 💡 Input validation and structured error handling
- 📦 Modular, maintainable project architecture
- ♻️ Docker support for easy containerized deployment
- 📡 Health check endpoint for uptime monitoring

---

## 📦 Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/ProjectUdaan.git
   cd ProjectUdaan
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service locally**
   ```bash
   python main.py
   ```

---

## 🧭 Translation Flow Diagram

<img src="docs/flowchart.png" alt="Translation Flow" width="500"/>

## 🏗️ Project Architecture

### 📁 Directory Structure
```
Translation Microservice/
├── config/
│   ├── __init__.py
│   ├── .env
│   └── settings.py
├── models/
│   ├── __init__.py
│   └── translation_models.py
├── routes/
│   ├── __init__.py
│   ├── health_routes.py
│   └── translation_routes.py
├── services/
│   ├── __init__.py
│   ├── database_service.py
│   └── translation_service.py
├── utils/
│   ├── __init__.py
│   ├── language_utils.py
│   └── validation_utils.py
├── tests/
│   └── test_translation_service.py
├── docker-compose.yml
├── Dockerfile
├── main.py
└── requirements.txt
```

### 🧩 Core Components

#### `main.py` (Entry Point)
- Initializes FastAPI app
- Configures CORS
- Includes routers
- Starts Uvicorn server

#### `routes/` (API Endpoints)
- `translation_routes.py`: Handles `/translate` endpoints
- `health_routes.py`: Service health monitoring

#### `services/` (Business Logic)
- `translation_service.py`: Core translation logic
- `database_service.py`: SQLite operations

#### `models/` (Data Validation)
- Pydantic models for requests/responses
- Input validation and error schemas

#### `utils/` (Helpers)
- `language_utils.py`: Language code validation
- `validation_utils.py`: Text sanitization

---

## 📘 API Endpoints

### Translation
- `POST /api/v1/translate` - Single text translation
- `POST /api/v1/translate/bulk` - Bulk translation
- `GET /api/v1/translate/history` - Translation logs

### Health
- `GET /api/v1/health` - Service status

---

## 🔄 Request Flow
1. Client → API Endpoint
2. Pydantic Validation
3. Translation Service Processing
4. Database Logging
5. Structured Response

---

## 🧪 Usage Examples

### Single Translation
```bash
curl -X POST "http://localhost:8000/api/v1/translate" \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","target_language":"ta"}'
```

### Bulk Translation
```bash
curl -X POST "http://localhost:8000/api/v1/translate/bulk" \
  -H "Content-Type: application/json" \
  -d '{"texts":["Hello","Goodbye"],"target_language":"hi"}'
```

---

## 🐳 Docker Deployment
```bash
docker-compose up -d
```

---

## 🛠️ Production Considerations
1. Integrate Google Translate API
2. Switch to PostgreSQL/MySQL
3. Add JWT authentication
4. Implement rate limiting
5. Set up monitoring (Prometheus/Grafana)

---

## 📝 Maintenance Notes
Clear cache when needed:
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

For Windows:
```powershell
Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force
```

Key Improvements:
1. Fixed utility filenames (removed 'tutils' typos)
2. Streamlined architecture overview
3. Maintained all functionality
4. Added clear maintenance commands
5. Organized content logically
```
