import re

def strip_code_fences(text: str) -> str:
    """Removes any Markdown code fences (```json ... ```) around a JSON blob."""
    text = text.strip()
    match = re.match(r"^```(?:json)?\s*(.*?)\s*```$", text, re.DOTALL)
    return match.group(1) if match else text