# src/prompts/summarisation_prompts.py — Log Summarisation Prompts
#
# PURPOSE:
#   Contains the prompt template for summarising long error logs.
#   Used when logs are too long even after regex filtering —
#   the LLM condenses them into a concise technical summary.
#
# WHEN USED:
#   Only triggered when the preprocessed log text exceeds a configurable
#   token threshold. Most reports won't need this step.
#
# TODO:
#   - Write the SUMMARISATION_SYSTEM_PROMPT
#   - Include instructions to preserve: error type, root cause, affected component
#   - Add max output length constraint

SUMMARISATION_SYSTEM_PROMPT = ""
