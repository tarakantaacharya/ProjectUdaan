
````markdown
# 🌍 Translation Microservice

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
````

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the service locally**

   ```bash
   python main.py
   ```

---

## 📘 API Endpoints

### 🔄 Translation

* `POST /api/v1/translate`
  Translate a single text block.

* `POST /api/v1/translate/bulk`
  Translate multiple texts in one request.

* `GET /api/v1/translate/history`
  View recent translation history.

### ❤️ Health Check

* `GET /api/v1/health`
  Returns service status.

---

## 🧪 Usage Examples

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

---

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

> Ensure Docker and Docker Compose are installed on your machine.

---

## 🧱 Project Architecture

```text
.
├── main.py                  # FastAPI app entry point
├── routes/                  # API route handlers
│   └── translation_routes.py
│   └── health_routes.py
├── services/                # Business logic
│   └── translation_service.py
│   └── database_service.py
├── models/                  # Pydantic request/response schemas
├── data/                    # Translation dictionaries (mock)
│   └── translation_data.py
├── utils/                   # Helper functions, validation
├── config/                  # Config settings (optional)
├── requirements.txt
└── docker-compose.yml
```

---

## 🛠️ Production Considerations

* 🔄 Replace mock data with the **Google Translate API**
* 🛢️ Use PostgreSQL or MySQL instead of SQLite
* 🔐 Add authentication and rate limiting
* 📈 Integrate logging and monitoring
* ✅ Add unit/integration tests with coverage
* 🔁 Set up CI/CD pipelines for deployment

---

## 📝 Notes

> ⚠️ **If you're unable to run the service or face unusual behavior**, clear Python caches to remove stale compiled files.

### Clear Cache:

On **Linux/macOS**:

```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

On **Windows (PowerShell)**:

```powershell
Get-ChildItem -Recurse -Include __pycache__ | Remove-Item -Recurse -Force
```
```
