import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from fastapi import HTTPException
from app.core.config import OUTPUT_DIR

ALLOWED_SUFFIXES = {".mp3", ".wav", ".flac", ".m4a", ".ogg", ".aac"}

def separate_audio(source: Path, mode: str) -> Path:
    """Run Demucs CLI when installed; raise a clear error otherwise."""
    executable = shutil.which("demucs")
    if not executable:
        raise HTTPException(
            status_code=503,
            detail="Audio separation is not configured. Install a compatible Demucs build and its audio dependencies first.",
        )
    if mode not in {"simple", "pro"}:
        raise HTTPException(status_code=422, detail="mode must be 'simple' or 'pro'")

    with tempfile.TemporaryDirectory(prefix="aiml_demucs_") as tmp:
        work = Path(tmp)
        command = [executable, "-o", str(work)]
        if mode == "simple":
            command += ["--two-stems", "vocals"]
        command += [str(source)]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=1800)
        except subprocess.TimeoutExpired as exc:
            raise HTTPException(status_code=504, detail="Audio separation exceeded the 30-minute processing limit.") from exc
        if result.returncode != 0:
            detail = (result.stderr or result.stdout or "Demucs processing failed")[-3000:]
            raise HTTPException(status_code=500, detail=f"Demucs failed: {detail}")

        produced = [p for p in work.rglob("*") if p.is_file()]
        if not produced:
            raise HTTPException(status_code=500, detail="Demucs completed but did not produce output files.")

        archive = OUTPUT_DIR / f"{source.stem}_stems.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for path in produced:
                zf.write(path, arcname=path.relative_to(work))
        return archive
