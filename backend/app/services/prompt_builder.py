from app.schemas.prompts import PromptBuildRequest

def _clean(values: list[str]) -> list[str]:
    return [v.strip() for v in values if v and v.strip()]

def build_prompt(data: PromptBuildRequest) -> str:
    """Create a transparent template-based prompt from the supplied fields."""
    parts: list[str] = []
    if data.mode == "instrumental":
        parts.append(f"Create an original instrumental music piece based on this concept: {data.idea}.")
    else:
        parts.append(f"Create an original song with vocals based on this concept: {data.idea}.")

    identity = [x for x in (data.genre, data.subgenre) if x and x.strip()]
    if identity:
        parts.append("Musical identity: " + " / ".join(identity) + ".")
    if data.mood:
        parts.append("Mood: " + ", ".join(_clean(data.mood)) + ".")
    if data.atmosphere:
        parts.append("Atmosphere: " + data.atmosphere.strip() + ".")
    if data.energy:
        parts.append("Energy: " + data.energy.strip() + ".")
    if data.instruments:
        parts.append("Instrumentation: " + ", ".join(_clean(data.instruments)) + ".")
    if data.tempo_bpm is not None:
        parts.append(f"Tempo: {data.tempo_bpm} BPM.")
    if data.groove:
        parts.append("Rhythm and groove: " + data.groove.strip() + ".")
    if data.mode == "vocal":
        vocal_details = [x for x in (data.vocal_style, data.lyrics_language) if x and x.strip()]
        if vocal_details:
            parts.append("Vocal direction: " + "; ".join(vocal_details) + ".")
    if data.structure:
        parts.append("Arrangement progression: " + " → ".join(_clean(data.structure)) + ".")
    if data.duration:
        parts.append("Target duration: " + data.duration.strip() + " (if supported by the generation service).")
    if data.production:
        parts.append("Production and mix: " + data.production.strip() + ".")
    if data.additional_instructions:
        parts.append("Additional instructions: " + data.additional_instructions.strip())
    parts.append("Keep the arrangement coherent, musically consistent, and faithful to the original concept.")
    return " ".join(parts)
