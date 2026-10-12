from typing import Literal
from pydantic import BaseModel, Field, field_validator

MusicMode = Literal["vocal", "instrumental"]

class PromptBuildRequest(BaseModel):
    mode: MusicMode = "instrumental"
    idea: str = Field(min_length=3, max_length=2000)
    genre: str | None = Field(default=None, max_length=100)
    subgenre: str | None = Field(default=None, max_length=100)
    mood: list[str] = Field(default_factory=list, max_length=10)
    atmosphere: str | None = Field(default=None, max_length=300)
    energy: str | None = Field(default=None, max_length=100)
    vocal_style: str | None = Field(default=None, max_length=200)
    lyrics_language: str | None = Field(default=None, max_length=80)
    instruments: list[str] = Field(default_factory=list, max_length=20)
    tempo_bpm: int | None = Field(default=None, ge=40, le=240)
    groove: str | None = Field(default=None, max_length=200)
    structure: list[str] = Field(default_factory=list, max_length=20)
    production: str | None = Field(default=None, max_length=300)
    duration: str | None = Field(default=None, max_length=80)
    additional_instructions: str | None = Field(default=None, max_length=1000)

    @field_validator("idea")
    @classmethod
    def idea_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("idea cannot be blank")
        return value

class PromptBuildResponse(BaseModel):
    mode: MusicMode
    prompt: str
    generation_ready: bool = True
    enhancement_method: Literal["rule_based", "external_ai"] = "rule_based"

class PromptEnhanceRequest(BaseModel):
    prompt: str = Field(min_length=3, max_length=5000)

class PromptEnhanceResponse(BaseModel):
    prompt: str
    enhancement_method: Literal["rule_based", "external_ai"]
    note: str
