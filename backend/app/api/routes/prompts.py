from fastapi import APIRouter
from app.schemas.prompts import (
    PromptBuildRequest, PromptBuildResponse,
    PromptEnhanceRequest, PromptEnhanceResponse,
)
from app.services.prompt_builder import build_prompt
from app.services.prompt_enhancer import enhance_prompt_rule_based

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.post("/build", response_model=PromptBuildResponse)
def build(data: PromptBuildRequest):
    return PromptBuildResponse(
        mode=data.mode,
        prompt=build_prompt(data),
        generation_ready=True,
        enhancement_method="rule_based",
    )

@router.post("/enhance", response_model=PromptEnhanceResponse)
def enhance(data: PromptEnhanceRequest):
    return PromptEnhanceResponse(
        prompt=enhance_prompt_rule_based(data.prompt),
        enhancement_method="rule_based",
        note="Offline rule-based normalization was used. No external AI model was called.",
    )
