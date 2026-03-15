# src/agents/extraction_agent.py — Raw Text → Structured JSON Agent
#
# PURPOSE:
#   Takes preprocessed (noise-filtered) bug report text and uses an LLM
#   (via LangChain) to extract structured information:
#     - Issue summary (one-line technical description)
#     - Steps to reproduce (ordered list, or "Not provided by user")
#     - Technical details (error messages, environment info)
#
# APPROACH:
#   Uses LangChain's structured output (with_structured_output) to
#   ensure the LLM returns data matching the TriageResult Pydantic model.
#   Prompts are imported from src/prompts/extraction_prompts.py.
#
# KEY CLASS:
#   ExtractionAgent — with methods like:
#     - extract(cleaned_text: str) → TriageResult
#
# IMPORTANT DESIGN DECISION:
#   If the user didn't provide steps to reproduce, the agent MUST return
#   "Steps not provided by user" — it should NEVER hallucinate steps.
#
# TODO:
#   - Initialise LangChain LLM with settings from src/config
#   - Build the chain: prompt | llm | structured_output_parser
#   - Implement the extract() method
#   - Add error handling and retry logic

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
