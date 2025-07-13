

<div align="center">

# 🌍 Translation Microservice

### FastAPI-powered Multi-Language Translation API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-green.svg)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Dockerized-Ready-blue.svg)](https://www.docker.com/)
[![SQLite](https://img.shields.io/badge/SQLite-Logging-lightgrey.svg)](https://sqlite.org/index.html)

**Real-time multilingual text translation built for scalability, performance, and simplicity.**
*Translate • Validate • Log • Scale*

[📖 API Docs](#-api-endpoints) • [🐳 Docker Setup](#-docker-deployment) • [⚙️ Architecture](#️-project-architecture) • [📂 Full Overview](#-project-details)

</div>

---

## 🎯 Project Summary

A lightweight, scalable microservice built with **FastAPI**, enabling multilingual translation (English, Tamil, Hindi, Kannada, Bengali). Designed for production-readiness with clean modular architecture, persistent storage (SQLite), Docker support, and health monitoring.

---

## ✨ Key Features

✅ REST API for single and bulk translation
🌐 Language Support: `ta`, `hi`, `kn`, `bn`
📊 SQLite logging of every request
🧩 Pydantic-based validation
🔁 Batch support (up to 50 texts)
📦 Docker-ready
📡 Health monitoring endpoint
📄 Auto-generated OpenAPI Docs

---

## 🚀 Quickstart

### 📥 Install & Run

```bash
git clone https://github.com/your-username/ProjectUdaan.git
cd ProjectUdaan
pip install -r requirements.txt
python main.py
```

### 🐳 Docker Deployment

```bash
docker-compose up -d
```

---

## 🧭 Translation Flow

<div align="center">
  <img src="docs/flowchart.png" alt="Translation Flow" width="500"/>
</div>

---

## 📘 API Endpoints

| Method | Endpoint                    | Description                     |
| ------ | --------------------------- | ------------------------------- |
| POST   | `/api/v1/translate`         | Translate a single text         |
| POST   | `/api/v1/translate/bulk`    | Translate multiple texts        |
| GET    | `/api/v1/translate/history` | Fetch translation logs          |
| GET    | `/api/v1/health`            | Service & database health check |

---

## 🧪 Sample Usage

### 🔹 Single Translation

```json
POST /api/v1/translate
{
  "text": "Hello",
  "target_language": "ta"
}
```

### 🔹 Bulk Translation

```json
POST /api/v1/translate/bulk
{
  "texts": ["Hello", "Goodbye"],
  "target_language": "hi"
}
```

---

## 🏗️ Project Architecture

A modular, scalable layout with a clean separation of concerns:

```
Translation Microservice
├── API Layer (FastAPI)
├── Business Logic Layer (Services)
├── Data Models Layer (Pydantic)
├── Data Persistence Layer (SQLite)
└── Utility Layer (Helpers & Validators)
```

---

## 📂 Project Details

### 🚀 Core Application Files

| File               | Purpose                                    |
| ------------------ | ------------------------------------------ |
| `main.py`          | FastAPI app setup, middleware, router init |
| `requirements.txt` | Project dependencies                       |
| `Dockerfile`       | Container build instructions               |
| `render.yml`       | Deployment config for Render               |

---

### 🛣️ `/routes` – API Layer

* `translation_routes.py`

  * `POST /translate`: Single translation
  * `POST /translate/bulk`: Bulk (max 50)
  * `GET /history`: Fetch logs
* `health_routes.py`

  * `GET /health`: Check service + DB status

---

### 🏢 `/services` – Business Logic Layer

* `translation_service.py`

  * Multi-language logic
  * UUID tracking
  * Mock translation (Google Translate ready)
* `database_service.py`

  * SQLite connection pool
  * Schema management + query ops

---

### 📊 `/models` – Pydantic Models

| Model                     | Purpose                    |
| ------------------------- | -------------------------- |
| `TranslationRequest`      | Single translation input   |
| `BulkTranslationRequest`  | Bulk input (1–50 max)      |
| `TranslationResponse`     | Single output format       |
| `BulkTranslationResponse` | Response for batch request |
| `ErrorResponse`           | Consistent error structure |

---

### 🔧 `/utils` – Utilities

* `lang_helper.py`:
  Language detection, code validation, registry
* `db_logger.py`:
  Transaction logging
* `validation_utils.py`:
  Sanitization, length validation

---

### ⚙️ `/config` – Environment Configuration

| File          | Use                              |
| ------------- | -------------------------------- |
| `settings.py` | Env config, OpenAPI meta, limits |

---

### 🧪 `/tests` – Quality Assurance

* `test_translation_service.py`: Translation logic unit tests
* `test_import.py`: Module import checks

---

### 📚 `/docs` – Documentation

* Accessible at `/docs` (Swagger) and `/redoc`
* Markdown + autogenerated API docs

---

## ⚙️ Technical Specifications

| Stack      | Tool                |
| ---------- | ------------------- |
| Framework  | FastAPI 0.110.0     |
| Server     | Uvicorn 0.24.0      |
| Validation | Pydantic 2.5.0      |
| DB         | SQLite (file-based) |
| Container  | Docker              |
| Deployment | Render              |

---

## ✅ API Capabilities

| Feature            | Status |
| ------------------ | ------ |
| Single Translation | ✅      |
| Bulk Translation   | ✅      |
| History Tracking   | ✅      |
| Health Monitoring  | ✅      |
| Google API Ready   | ✅      |
| Input Validation   | ✅      |
| Auto API Docs      | ✅      |
| CORS Support       | ✅      |

---

## 🚀 Deployment & Operations

* Dockerized: `docker-compose.yml`, `Dockerfile`
* Ready for Render: `render.yml` config
* Health checks for uptime monitoring
* Structured logs for debugging
* Environment-based flexibility

---

## 🛠️ Production Readiness

✔️ Scalable Architecture
✔️ Logging & Monitoring
✔️ Containerization
✔️ CI/CD-ready
✔️ Google Translate Integration Ready
✔️ Secure & Validated Inputs
✔️ Full Swagger Documentation

---

<div align="center">

### ✅ Built with FastAPI • Designed for Scale • Easy to Extend

🌟 *If you find this useful, give it a ⭐ and share feedback!*

</div>


