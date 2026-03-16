"""
src/agents/extraction_agent.py — Extraction LangGraph Node
------------------------------------------------------------
PURPOSE:
    LangGraph node that takes preprocessed text and produces
    a structured TriageResult using the LLM.

WHAT IT DOES:
    1. Reads cleaned_text + user_review from PipelineState
    2. Builds a prompt using extraction_prompts
    3. Calls the LLM with structured output (ExtractionResult schema)
    4. Returns the extraction result back to PipelineState

CAPABILITIES (can be extended later):
    - Few-shot examples in the prompt
    - Retry logic on malformed output
    - Chain-of-thought reasoning before extraction
    - Multi-language support

CONNECTS TO:
    - orchestrator.py registers this as the "extract" node
    - Uses agent.py's LLMManager for the LLM client
    - Uses prompts/extraction_prompts.py for prompt templates
    - Outputs into schemas/triage_output.ExtractionResult
"""

# Use PydanticOutputParser only to get format instructions (helps non-compliant models)
# from langchain_core.output_parsers import PydanticOutputParser

from langchain_core.prompts import ChatPromptTemplate

from src.agents.agent import LLMManager
from src.prompts.extraction_prompts import (
    EXTRACTION_SYSTEM_PROMPT,
    EXTRACTION_USER_PROMPT,
)
from src.schemas.triage_output import ExtractionResult
from src.telemetry.logger import get_logger

logger = get_logger(__name__)


def run_extraction(state: dict) -> dict:
    """LangGraph node: extract structured data from the bug report.

    Reads from state:
        - cleaned_text: str
        - user_review: str (optional)
        - signals: dict

    Writes to state:
        - extraction_result: ExtractionResult
    """
    cleaned_text = state.get("cleaned_text", "")
    user_review = state.get("user_review", "No user review provided")
    signals = state.get("signals", {})

    logger.info("Running extraction agent...")

    # Build the prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXTRACTION_SYSTEM_PROMPT),
        ("human", EXTRACTION_USER_PROMPT),
    ])

    # Get LLM with structured output
    llm_manager = LLMManager()
    structured_llm = llm_manager.get_client_with_structured_output(ExtractionResult)

    # Build and invoke the chain
    # We add format_instructions to the system prompt dynamically
    chain = prompt | structured_llm
    result = chain.invoke({
        "bug_report_text": cleaned_text,
        "user_review": user_review or "No user review provided",
        "signals": str(signals)
    })

    logger.info(f"Extraction complete: {result.issue_summary}")
    logger.info(f'')
    return {"extraction_result": result}