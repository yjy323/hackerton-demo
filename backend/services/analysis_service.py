"""Analysis service for contract summarization and risk detection."""
import json
from datetime import datetime
from pathlib import Path

from config import get_openai_client, get_settings
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

    # Generate summary
    summary = await _summarize_content(stt_text, ocr_text)

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


async def _summarize_content(stt_text: str, ocr_text: str) -> str:
    """
    Generate AI summary of combined STT and OCR content.

    Args:
        stt_text: Transcribed speech text
        ocr_text: Extracted document text

    Returns:
        AI-generated summary
    """
    settings = get_settings()
    client = get_openai_client()

    combined_text = f"[음성 대화]\n{stt_text}\n\n[문서 내용]\n{ocr_text}"

    response = client.chat.completions.create(
        model=settings.openai_model_name,
        messages=[
            {
                "role": "system",
                "content": "당신은 계약서와 대화 내용을 요약하는 전문가입니다. 핵심 내용을 간결하게 요약하세요.",
            },
            {"role": "user", "content": f"다음 내용을 요약해주세요:\n\n{combined_text}"},
        ],
    )

    return response.choices[0].message.content.strip()
