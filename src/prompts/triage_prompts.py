# src/prompts/triage_prompts.py — Triage Agent Prompts
#
# PURPOSE:
#   Contains the system and user prompt templates for the Triage Agent.
#   The triage agent classifies severity (P1–P4) and assigns team ownership.
#
# PROMPT DESIGN PRINCIPLES:
#   - System prompt includes the severity policy and team routing rules
#   - The policy is loaded from src/policies/ YAML files
#   - User prompt injects the extracted structured data
#   - Classification must be objective — based on rules, not user emotion
#
# TODO:
#   - Write the TRIAGE_SYSTEM_PROMPT with policy placeholder
#   - Write the TRIAGE_USER_PROMPT with {extracted_data} placeholder
#   - Include few-shot examples of P1 vs P3 classification

TRIAGE_SYSTEM_PROMPT = ""
TRIAGE_USER_PROMPT = ""
