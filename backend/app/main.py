from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.routes.health import router as health_router
from app.api.routes.prompts import router as prompts_router
from app.api.routes.music import router as music_router
from app.api.routes.audio import router as audio_router
from app.core.config import settings

# ۱. فقط یک بار app را تعریف کنید
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Backend for AI Music Lab. Prompt building works locally; external AI/audio providers are optional.",
)

# ۲. مسیر ریشه را به همین app اضافه کنید
@app.get("/")
def read_root():
    return {"message": "Hello, this is your AI Music Lab API"}

# ۳. سایر تنظیمات را به همین app اضافه کنید
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(prompts_router, prefix="/api/v1")
app.include_router(music_router, prefix="/api/v1")
app.include_router(audio_router, prefix="/api")

# Serve the existing single-file frontend at /ui
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
if FRONTEND_DIR.exists() and (FRONTEND_DIR / "index.html").exists():
    app.mount("/ui", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
