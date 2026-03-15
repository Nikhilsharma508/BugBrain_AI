# src/prompts — Prompt Templates
#
# This package stores all LLM prompt templates, separated from agent logic.
# Prompts are defined as string constants or ChatPromptTemplate objects.
#
# Exports:
#   - EXTRACTION_SYSTEM_PROMPT, EXTRACTION_USER_PROMPT
#   - TRIAGE_SYSTEM_PROMPT, TRIAGE_USER_PROMPT
#   - SUMMARISATION_SYSTEM_PROMPT

from src.prompts.extraction_prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT,
)
from src.prompts.triage_prompts import (
    TRIAGE_SYSTEM_PROMPT,
    TRIAGE_USER_PROMPT,
)
from src.prompts.summarisation_prompts import (
    SUMMARISATION_SYSTEM_PROMPT,
)

__all__ = [
    "EXTRACTION_SYSTEM_PROMPT",
    "EXTRACTION_USER_PROMPT",
    "TRIAGE_SYSTEM_PROMPT",
    "TRIAGE_USER_PROMPT",
    "SUMMARISATION_SYSTEM_PROMPT",
]
