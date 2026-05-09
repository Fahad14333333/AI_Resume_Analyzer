import re
from fastapi import HTTPException
from app.core.config import settings

PHONE_REGEX = re.compile(r"\+?\d[\d\s\-()]{7,}\d")
EMAIL_REGEX = re.compile(r"[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}")
NAME_REGEX = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3}$")


def validate_file_extension(filename: str):
    if "." not in filename:
        raise HTTPException(status_code=400, detail="Invalid file name.")
    ext = filename.rsplit(".", 1)[1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
    return ext


def validate_file_size(size: int):
    if size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=413, detail="File exceeds maximum upload size.")


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
