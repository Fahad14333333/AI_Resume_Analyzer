import io
import re
from fastapi import HTTPException, UploadFile
from pdfplumber import open as open_pdf
from docx import Document
from PIL import Image
import pytesseract

from app.core.security import validate_file_extension, validate_file_size, normalize_text
from app.core.config import settings


class FileService:
    @staticmethod
    async def extract_resume_text(upload_file: UploadFile) -> str:
        await upload_file.seek(0)
        content = await upload_file.read()
        validate_file_size(len(content))
        ext = validate_file_extension(upload_file.filename)
        if ext == "pdf":
            return FileService._extract_text_pdf(content)
        if ext == "docx":
            return FileService._extract_text_docx(content)
        raise HTTPException(status_code=400, detail="Unsupported file content.")

    @staticmethod
    def _extract_text_pdf(raw_bytes: bytes) -> str:
        with io.BytesIO(raw_bytes) as buffer:
            try:
                with open_pdf(buffer) as pdf:
                    return "\n".join(page.extract_text() or "" for page in pdf.pages)
            except Exception:
                return FileService._extract_text_ocr(buffer)

    @staticmethod
    def _extract_text_docx(raw_bytes: bytes) -> str:
        with io.BytesIO(raw_bytes) as buffer:
            try:
                doc = Document(buffer)
                return "\n".join(paragraph.text for paragraph in doc.paragraphs)
            except Exception as exc:
                raise HTTPException(status_code=400, detail=f"Unable to parse DOCX: {exc}")

    @staticmethod
    def _extract_text_ocr(buffer: io.BytesIO) -> str:
        try:
            image = Image.open(buffer)
            return pytesseract.image_to_string(image, lang="eng+urd")
        except Exception:
            return ""

    @staticmethod
    def sanitize_upload_text(text: str) -> str:
        return normalize_text(re.sub(r"[\r\t]+", " ", text))
