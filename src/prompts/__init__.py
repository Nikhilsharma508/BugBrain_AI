"""src/prompts — Prompt Templates."""

from src.prompts.extraction_prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT,
)
from src.prompts.triage_prompts import (
    TRIAGE_SYSTEM_PROMPT,
    TRIAGE_USER_PROMPT,
)

__all__ = [
    "EXTRACTION_SYSTEM_PROMPT",
    "EXTRACTION_USER_PROMPT",
    "TRIAGE_SYSTEM_PROMPT",
    "TRIAGE_USER_PROMPT",
]
