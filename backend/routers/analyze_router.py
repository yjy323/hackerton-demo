"""Analysis endpoints for contract processing."""
from fastapi import APIRouter, Depends, HTTPException

from config import Settings, get_settings
from schemas import AnalysisResponse, ErrorResponse
from services.analysis_service import analyze_session

router = APIRouter(tags=["analysis"])


@router.post(
    "/analyze/session/{session_id}",
    response_model=AnalysisResponse,
    responses={404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Analyze contract session",
    description="Analyze combined STT and OCR data for a session using AI.",
)
async def analyze_contract(
    session_id: str,
    settings: Settings = Depends(get_settings),
) -> AnalysisResponse:
    """Analyze contract data from STT and OCR sources."""
    try:
        result = await analyze_session(session_id, settings.storage_base_path)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Session not found: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
