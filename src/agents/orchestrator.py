# src/agents/orchestrator.py — End-to-End Pipeline Controller
#
# PURPOSE:
#   The central coordinator that chains all components together into
#   a single pipeline. This is the function that both the Streamlit UI
#   and any future API would call.
#
# PIPELINE FLOW:
#   1. TextCleaner → normalise the raw input
#   2. NoiseFilter → strip irrelevant content
#   3. LogParser → extract technical signals
#   4. ExtractionAgent → LLM-based structured extraction
#   5. DuplicateDetection → check for existing similar reports
#   6. TriageAgent → severity + team classification
#   7. Return final TriageResult
#
# KEY FUNCTION:
#   run_pipeline(raw_text: str) → TriageResult
#
# DESIGN:
#   The orchestrator is designed so that any external interface
#   (Streamlit, FastAPI, CLI) simply calls run_pipeline() —
#   making it trivial to add new frontends without changing logic.
#
# TODO:
#   - Import and initialise all components
#   - Implement run_pipeline() with proper error handling
#   - Add telemetry hooks (latency, token tracking)
#   - Add LangChain callback for cost tracking

from typing import Optional
