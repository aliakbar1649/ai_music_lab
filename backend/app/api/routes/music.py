from fastapi import APIRouter, HTTPException
from app.core.config import settings

router = APIRouter(prefix="/music", tags=["music"])

@router.post("/generations", status_code=503)
def create_generation():
    # Deliberately do not create fake job IDs or pretend audio was generated.
    raise HTTPException(
        status_code=503,
        detail={
            "code": "MUSIC_PROVIDER_NOT_CONFIGURED",
            "message": "Real music generation is not configured. Select and configure a provider before enabling this endpoint.",
        },
    )
