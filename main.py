from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes.translation_routes import router as translation_router
from routes.health_routes import router as health_router
from services.database_service import init_db
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Translation Microservice",
    description="A lightweight, modular translation service",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
from services.database_service import init_db
init_db()

# Include routers
app.include_router(translation_router, prefix="/api/v1", tags=["translation"])
app.include_router(health_router, prefix="/api/v1", tags=["health"])

@app.get("/")
async def root():
    return {"message": "Translation Microservice", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)