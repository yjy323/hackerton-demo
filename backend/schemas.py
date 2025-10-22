"""Pydantic models for request/response validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    """Response model for file upload endpoints."""

    session_id: str = Field(..., description="Unique session identifier")
    text_preview: str = Field(..., description="Preview of extracted text (truncated)")
    text_length: int = Field(..., description="Full length of extracted text")


class AnalysisResponse(BaseModel):
    """Response model for analysis endpoint."""

    session_id: str = Field(..., description="Session identifier")
    stt_text: str = Field(..., description="Full transcribed speech text")
    ocr_text: str = Field(..., description="Full OCR extracted text")
    summary: str = Field(..., description="AI-generated summary")
    timestamp: datetime = Field(..., description="Analysis timestamp")


class ErrorResponse(BaseModel):
    """Standard error response model."""

    detail: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code for client handling")
