import os
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[3]

def _csv_env(name: str, default: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "AI Music Lab")
    environment: str = os.getenv("APP_ENV", "development")
    max_audio_upload_mb: int = int(os.getenv("MAX_AUDIO_UPLOAD_MB", "100"))
    cors_origins: list[str] = None

    def __post_init__(self):
        object.__setattr__(self, "cors_origins", _csv_env("CORS_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000"))

settings = Settings()
STORAGE_DIR = ROOT_DIR / "storage"
UPLOAD_DIR = STORAGE_DIR / "uploads"
OUTPUT_DIR = STORAGE_DIR / "outputs"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
