"""Upload endpoints for audio and document files."""
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile

from config import Settings, get_settings
from schemas import ErrorResponse, UploadResponse
from services.ocr_service import extract_text_from_file
from services.stt_service import transcribe_audio

router = APIRouter(tags=["upload"])


@router.post(
    "/upload/audio",
    response_model=UploadResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Upload and transcribe audio file",
    description="Upload an audio file and transcribe it using OpenAI Whisper API.",
)
async def upload_audio(
    session_id: str = Form(..., description="Unique session identifier"),
    file: UploadFile = File(..., description="Audio file (WAV, MP3, etc.)"),
    settings: Settings = Depends(get_settings),
) -> UploadResponse:
    """Upload and transcribe audio file."""
    try:
        session_dir = Path(settings.storage_base_path) / session_id
        text = await transcribe_audio(file, session_dir)

        return UploadResponse(
            session_id=session_id,
            text_preview=text[:200] + "..." if len(text) > 200 else text,
            text_length=len(text),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio transcription failed: {str(e)}")


@router.post(
    "/upload/document",
    response_model=UploadResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Upload and extract text from document",
    description="Upload an image or PDF and extract text using OCR.",
)
async def upload_document(
    session_id: str = Form(..., description="Unique session identifier"),
    file: UploadFile = File(..., description="Image or PDF file"),
    settings: Settings = Depends(get_settings),
) -> UploadResponse:
    """Upload and extract text from image or PDF."""
    try:
        session_dir = Path(settings.storage_base_path) / session_id
        text = await extract_text_from_file(file, session_dir)

        return UploadResponse(
            session_id=session_id,
            text_preview=text[:200] + "..." if len(text) > 200 else text,
            text_length=len(text),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document processing failed: {str(e)}")
