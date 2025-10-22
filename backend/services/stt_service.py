"""Speech-to-text service using OpenAI Whisper API."""
import tempfile
from pathlib import Path

from fastapi import UploadFile

from config import get_openai_client, get_settings


async def transcribe_audio(file: UploadFile, session_dir: Path) -> str:
    """
    Transcribe audio file to text using OpenAI Whisper.

    Args:
        file: Uploaded audio file
        session_dir: Directory to store transcription results

    Returns:
        Transcribed text

    Note:
        Multiple recordings are appended to stt.txt file.
    """
    session_dir.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    client = get_openai_client()

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        # Transcribe using Whisper
        with open(tmp_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model=settings.whisper_model,
                file=audio_file,
                language="ko",
            )

        text = result.text.strip()

        # Append to session STT file
        output_path = session_dir / "stt.txt"
        with open(output_path, "a", encoding="utf-8") as f:
            f.write(f"\n{text}")

        return text

    finally:
        # Clean up temporary file
        tmp_path.unlink(missing_ok=True)
