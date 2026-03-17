"""
src/agents/triage_agent.py — Triage LangGraph Node
----------------------------------------------------
PURPOSE:
    LangGraph node that classifies severity (P1–P4) and assigns
    team ownership based on the extraction result.

WHAT IT DOES:
    1. Loads severity_policy.yaml and team_routing.yaml
    2. Injects the policy rules into the triage prompt
    3. Feeds the extraction result to the LLM
    4. Returns severity + suggested_owner

HOW POLICIES ARE USED:
    - YAML files are loaded ONCE at module import time
    - Their text content is injected into the system prompt
    - The LLM classifies based on these rules, not its own judgment
    - To change rules: edit YAML → restart app

CAPABILITIES (can be extended later):
    - Confidence scoring for severity assignment
    - Multi-label classification (primary + secondary team)
    - Human-in-the-loop review for P1 severity
    - Historical accuracy tracking

CONNECTS TO:
    - orchestrator.py registers this as the "triage" node
    - Uses agent.py's LLMManager for the LLM client
    - Uses prompts/triage_prompts.py for prompt templates
    - Reads from src/policies/*.yaml
"""
# Use PydanticOutputParser for format instructions (helps non-compliant models)
from langchain_core.output_parsers import PydanticOutputParser

from pathlib import Path

import yaml
from langchain_core.prompts import ChatPromptTemplate

from src.agents.agent import LLMManager
from src.prompts.triage_prompts import TRIAGE_SYSTEM_PROMPT, TRIAGE_USER_PROMPT
from src.schemas.triage_output import ExtractionResult, ClassificationResult
from src.telemetry.logger import get_logger

logger = get_logger(__name__)

# --- Load policies at module level (once) ---
_POLICIES_DIR = Path(__file__).parent.parent / "policies"


def _load_yaml(filename: str) -> str:
    """Load a YAML file and return its content as a readable string."""
    filepath = _POLICIES_DIR / filename
    if not filepath.exists():
        logger.warning(f"Policy file not found: {filepath}")
        return "No policy file found."
    with open(filepath, "r") as f:
        data = yaml.safe_load(f)
    return yaml.dump(data, default_flow_style=False)


SEVERITY_POLICY_TEXT = _load_yaml("severity_policy.yaml")
TEAM_ROUTING_TEXT = _load_yaml("team_routing.yaml")


def run_triage(state: dict) -> dict:
    """LangGraph node: classify severity and assign team.

    Reads from state:
        - extraction_result: ExtractionResult

    Writes to state:
        - triage_result: ClassificationResult
    """
    extraction_result: ExtractionResult = state.get("extraction_result")
    if extraction_result is None:
        logger.error("No extraction result found in state")
        return {"triage_result": ClassificationResult()}

    logger.info("Running triage agent...")

    # Build the prompt with policies injected
    prompt = ChatPromptTemplate.from_messages([
        ("system", TRIAGE_SYSTEM_PROMPT),
        ("human", TRIAGE_USER_PROMPT),
    ])

    # Generate format instructions for non-compliant local models
    parser = PydanticOutputParser(pydantic_object=ClassificationResult)
    format_instructions = parser.get_format_instructions()

    # Get LLM with structured output
    llm_manager = LLMManager()
    structured_llm = llm_manager.get_client_with_structured_output(ClassificationResult)

    # Build and invoke the chain
    chain = prompt | structured_llm
    result = chain.invoke({
        "severity_policy": SEVERITY_POLICY_TEXT,
        "team_routing": TEAM_ROUTING_TEXT,
        "extracted_data": extraction_result.model_dump_json(indent=2),
        "format_instructions": format_instructions,
    })

    logger.info(f"Triage complete: severity={result.severity}, owner={result.suggested_owner}")

    return {"triage_result": result}
