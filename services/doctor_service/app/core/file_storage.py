"""
File storage utility for the doctor-service.
Saves uploaded files to a local `uploads/` directory.
In production, swap this for AWS S3 / Azure Blob.
"""
import uuid
import os
from pathlib import Path
from fastapi import UploadFile, HTTPException

# Root upload directory relative to project root
UPLOADS_BASE = Path(__file__).resolve().parent.parent.parent.parent.parent / "uploads"

ALLOWED_LICENSE_TYPES = {"application/pdf", "image/jpeg", "image/png", "image/jpg"}
ALLOWED_KYC_TYPES = {"application/pdf", "image/jpeg", "image/png", "image/jpg"}
MAX_FILE_SIZE_MB = 10


async def save_upload(file: UploadFile, subfolder: str) -> tuple[str, str]:
    """
    Save an uploaded file to the local uploads directory.
    Returns (file_url, file_type) where file_type is 'pdf' or 'image'.
    """
    if file.content_type not in ALLOWED_LICENSE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' not allowed. Must be PDF or image (JPG/PNG)."
        )

    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=400,
            detail=f"File too large ({size_mb:.1f}MB). Max is {MAX_FILE_SIZE_MB}MB."
        )

    # Determine type label
    file_type = "pdf" if file.content_type == "application/pdf" else "image"

    # Build save directory
    save_dir = UPLOADS_BASE / subfolder
    save_dir.mkdir(parents=True, exist_ok=True)

    # Unique filename
    ext = Path(file.filename or "file").suffix or (".pdf" if file_type == "pdf" else ".jpg")
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = save_dir / filename

    with open(file_path, "wb") as f:
        f.write(contents)

    # Return the relative URL that can be served
    relative_url = f"/uploads/{subfolder}/{filename}"
    return relative_url, file_type


def delete_upload(file_url: str):
    """Delete a previously saved upload by its relative URL."""
    try:
        relative = file_url.lstrip("/")
        full_path = UPLOADS_BASE.parent / relative
        if full_path.exists():
            os.remove(full_path)
    except Exception:
        pass  # Non-critical; log in production
