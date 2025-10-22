"""Analysis service for contract summarization and risk detection using CrewAI."""
import json
from datetime import datetime
from pathlib import Path

from agents import analyze_contract
from schemas import AnalysisResponse

async def analyze_session(session_id: str, base_path: str) -> AnalysisResponse:
    """
    Analyze session data by combining STT and OCR results.

    Args:
        session_id: Unique session identifier
        base_path: Base storage path for sessions

    Returns:
        Analysis results with summary

    Raises:
        FileNotFoundError: If session directory doesn't exist
    """
    session_dir = Path(base_path) / session_id

    if not session_dir.exists():
        raise FileNotFoundError(f"Session directory not found: {session_id}")

    # Read STT and OCR texts
    stt_path = session_dir / "stt.txt"
    ocr_path = session_dir / "ocr.txt"

    stt_text = stt_path.read_text(encoding="utf-8") if stt_path.exists() else ""
    ocr_text = ocr_path.read_text(encoding="utf-8") if ocr_path.exists() else ""

    # Generate summary using CrewAI agents
    summary = analyze_contract(stt_text, ocr_text)

    # Create analysis result
    result = AnalysisResponse(
        session_id=session_id,
        stt_text=stt_text,
        ocr_text=ocr_text,
        summary=summary,
        timestamp=datetime.now(),
    )

    # Save analysis results
    analysis_path = session_dir / "analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, ensure_ascii=False, indent=2, default=str)

    return result
