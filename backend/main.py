"""
Contract Assistant MVP - FastAPI Application

A real estate contract verification assistant that combines:
- Speech-to-Text (STT) using OpenAI Whisper
- OCR using GPT-4o Vision
- AI-powered contract analysis and summarization
"""
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import get_settings
from routers import analyze_router, upload_router

# Load environment variables
load_dotenv()

# Get application settings
settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Real estate contract verification assistant with STT, OCR, and AI analysis",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(upload_router.router, prefix="/api")
app.include_router(analyze_router.router, prefix="/api")

# Mount frontend static files (must be last)
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
