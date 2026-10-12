from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from app.core.config import settings, UPLOAD_DIR
from app.services.audio_processor import ALLOWED_SUFFIXES, separate_audio

router = APIRouter(tags=["audio"])

@router.post("/separate")
async def separate(
    file: UploadFile = File(...),
    mode: str = Query("simple", pattern="^(simple|pro)$"),
    lang: str = Query("en"),
):
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise HTTPException(status_code=415, detail="Unsupported audio format. Use MP3, WAV, FLAC, M4A, OGG, or AAC.")
    limit = settings.max_audio_upload_mb * 1024 * 1024
    content = await file.read(limit + 1)
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > limit:
        raise HTTPException(status_code=413, detail=f"File exceeds the {settings.max_audio_upload_mb} MB upload limit.")
    saved = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    saved.write_bytes(content)
    try:
        archive = separate_audio(saved, mode)
        return FileResponse(
            archive,
            media_type="application/zip",
            filename=archive.name,
            background=None,
        )
    finally:
        # Keep only the output archive. Uploaded source files are removed.
        saved.unlink(missing_ok=True)
