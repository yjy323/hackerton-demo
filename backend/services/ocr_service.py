"""OCR service for extracting text from images and PDFs using GPT-4o Vision."""
import base64
import tempfile
from pathlib import Path

from fastapi import UploadFile

from config import get_openai_client, get_settings

async def extract_text_from_file(file: UploadFile, session_dir: Path) -> str:
    """
    Extract text from image or PDF file using OCR.

    Args:
        file: Uploaded image or PDF file
        session_dir: Directory to store OCR results

    Returns:
        Extracted text content
    """
    session_dir.mkdir(parents=True, exist_ok=True)
    settings = get_settings()
    client = get_openai_client()

    filename = file.filename.lower()
    suffix = ".pdf" if filename.endswith(".pdf") else ".jpg"

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    try:
        text = await _process_file(client, tmp_path, suffix, settings)

        # Save OCR result
        output_path = session_dir / "ocr.txt"
        output_path.write_text(text, encoding="utf-8")

        return text

    finally:
        # Clean up temporary file
        tmp_path.unlink(missing_ok=True)


async def _process_file(client, tmp_path: Path, suffix: str, settings) -> str:
    """Process PDF or image file and extract text."""
    if suffix == ".pdf":
        return await _process_pdf(client, tmp_path, settings)
    else:
        return await _process_image(client, tmp_path, settings)


async def _process_pdf(client, pdf_path: Path, settings) -> str:
    """Process PDF file using Vision API or fallback to PyPDF2."""
    try:
        from pdf2image import convert_from_path
        import io

        images = convert_from_path(str(pdf_path))
        text_parts = []

        for image in images:
            # Convert image to base64
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format="PNG")
            base64_image = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

            # Extract text using Vision API
            response = client.chat.completions.create(
                model=settings.openai_model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "이 PDF 페이지에서 모든 텍스트를 정확히 추출해주세요. 텍스트만 반환하고 다른 설명은 하지 마세요.",
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                            },
                        ],
                    }
                ],
            )
            text_parts.append(response.choices[0].message.content.strip())

        return "\n\n".join(text_parts)

    except ImportError:
        # Fallback to PyPDF2 for text-based PDFs
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(str(pdf_path))
            text_parts = [page.extract_text() for page in reader.pages]
            text = "\n".join(text_parts)

            if not text.strip():
                return "PDF에서 텍스트를 추출할 수 없습니다. 스캔된 PDF의 경우 'pip install pdf2image'를 실행하세요."

            return text

        except Exception as e:
            return f"PDF 처리 중 오류 발생: {str(e)}"


async def _process_image(client, image_path: Path, settings) -> str:
    """Process image file using Vision API."""
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=settings.openai_model_name,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "이미지에서 모든 텍스트를 추출해주세요."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
    )

    return response.choices[0].message.content.strip()
