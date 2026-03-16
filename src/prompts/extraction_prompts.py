"""
src/prompts/extraction_prompts.py — Extraction Agent Prompts
-------------------------------------------------------------
PURPOSE:
    System + user prompt templates for the extraction agent.
    The LLM reads a bug report and produces structured JSON.

DESIGN:
    - Simple, 5-6 lines — concise instructions
    - Anti-hallucination rule: if steps not provided, say so honestly
    - Uses {bug_report_text} and {user_review} placeholders

CONNECTS TO:
    - agents/extraction_agent.py uses these prompts
"""

EXTRACTION_SYSTEM_PROMPT = """You are a software engineer that reads bug reports and extracts structured information.
MANDATORY: YOU MUST RETURN ONLY VALID JSON. DO NOT INCLUDE ANY CONVERSATIONAL TEXT, PREAMBLE, OR EXPLANATION.
Given a bug report, extract: issue summary (one line), steps to reproduce (ordered list), and technical details.
If steps to reproduce are NOT mentioned in the report or user review, return ["Not provided by user"]. Never guess steps.
Return only facts from the text. Do not add information that is not present.
"""

EXTRACTION_USER_PROMPT = """Bug Report:
{bug_report_text}

User Review:
{user_review}

Pre-extracted Signals (for reference):
{signals}"""
