from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health")
@router.get("/api/health", include_in_schema=False)  # compatibility with the supplied HTML
def health():
    return {"status": "ok", "service": "AI Music Lab"}
