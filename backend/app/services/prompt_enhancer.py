def enhance_prompt_rule_based(prompt: str) -> str:
    """Honest offline fallback: lightly normalize wording; this is not an AI model."""
    text = " ".join(prompt.split()).strip()
    if not text:
        raise ValueError("prompt cannot be blank")
    if not text.endswith((".", "!", "?")):
        text += "."
    return text
