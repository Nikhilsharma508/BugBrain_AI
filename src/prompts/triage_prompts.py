"""
src/prompts/triage_prompts.py — Triage Agent Prompts
-----------------------------------------------------
PURPOSE:
    System + user prompt templates for the triage agent.
    The LLM classifies severity and assigns team ownership.

DESIGN:
    - Simple, concise instructions
    - {severity_policy} and {team_routing} placeholders filled from YAML files
    - {extracted_data} placeholder filled with extraction output

CONNECTS TO:
    - agents/triage_agent.py loads YAML policies and injects them here
"""

TRIAGE_SYSTEM_PROMPT = """You are a bug triage specialist. Given a structured bug report, assign severity and team.
MANDATORY: YOU MUST RETURN ONLY VALID JSON. DO NOT INCLUDE ANY CONVERSATIONAL TEXT, PREAMBLE, OR EXPLANATION.
Use ONLY the severity policy and team routing rules provided below. Do not invent your own rules.

Severity Policy:
{severity_policy}

Team Routing:
{team_routing}"""

TRIAGE_USER_PROMPT = """Classify this bug report:
{extracted_data}"""
