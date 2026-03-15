# src/prompts/extraction_prompts.py — Extraction Agent Prompts
#
# PURPOSE:
#   Contains the system and user prompt templates for the Extraction Agent.
#   The extraction agent converts preprocessed bug report text into
#   structured JSON matching the TriageResult schema.
#
# PROMPT DESIGN PRINCIPLES:
#   - System prompt defines the agent's role and output format
#   - User prompt injects the actual bug report text
#   - Explicit instruction: NEVER hallucinate steps to reproduce
#   - Output must match the Pydantic schema exactly
#
# TODO:
#   - Write the EXTRACTION_SYSTEM_PROMPT with role, rules, and output format
#   - Write the EXTRACTION_USER_PROMPT with the {bug_report_text} placeholder
#   - Add few-shot examples if needed for better extraction quality

EXTRACTION_SYSTEM_PROMPT = ""
EXTRACTION_USER_PROMPT = ""
