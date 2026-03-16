"""
src/agents/orchestrator.py — LangGraph Pipeline Controller
------------------------------------------------------------
PURPOSE:
    The central controller that defines and runs the LangGraph StateGraph.
    This is the SINGLE entry point — Streamlit, FastAPI, CLI all call run_pipeline().

PIPELINE FLOW:
    preprocess_node → extract_node → triage_node → END

PIPELINESTATE FIELDS:
    - bug_trace: str (original bug report)
    - user_review: str (optional user commentary)
    - cleaned_text: str (after preprocessing)
    - signals: dict (extracted log signals)
    - extraction_result: ExtractionResult (after LLM extraction)
    - triage_result: ClassificationResult (final output with severity + team)

CAPABILITIES (can be extended later):
    - Add new nodes (duplicate_detection, summarisation) between existing ones
    - Add conditional edges (skip triage if duplicate detected)
    - Add parallel branches (run extraction + duplicate check simultaneously)
    - Add human-in-the-loop approval for P1 severity
    - Add retry nodes for failed LLM calls

CONNECTS TO:
    - preprocessing/__init__.py for the preprocess step
    - agents/extraction_agent.py for the extract step
    - agents/triage_agent.py for the triage step
    - main.py or ui/app.py calls run_pipeline()
"""

from typing import Optional
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

from src.preprocessing import run_preprocessing
from src.agents.extraction_agent import run_extraction
from src.agents.triage_agent import run_triage
from src.schemas.triage_output import TriageResult, ExtractionResult, ClassificationResult
from src.telemetry.logger import get_logger

logger = get_logger(__name__)


# --- Pipeline State ---
class PipelineState(TypedDict, total=False):
    """Shared state passed between LangGraph nodes."""

    bug_trace: str
    user_review: Optional[str]
    cleaned_text: str
    signals: dict
    extraction_result: ExtractionResult
    triage_result: ClassificationResult


# --- Node Functions ---
def preprocess_node(state: dict) -> dict:
    """LangGraph node: run preprocessing pipeline."""
    bug_trace = state.get("bug_trace", "")
    logger.info("Running preprocessing...")

    result = run_preprocessing(bug_trace)

    return {
        "cleaned_text": result["cleaned_text"],
        "signals": result["signals"],
    }


# --- Build the Graph ---
def build_pipeline() -> StateGraph:
    """Build and compile the LangGraph pipeline."""
    graph = StateGraph(PipelineState)

    # Add nodes
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("extract", run_extraction)
    graph.add_node("triage", run_triage)

    # Define edges: START → preprocess → extract → triage → END
    graph.add_edge(START, "preprocess")
    graph.add_edge("preprocess", "extract")
    graph.add_edge("extract", "triage")
    graph.add_edge("triage", END)

    return graph.compile()


# Compile once at import
pipeline = build_pipeline()


# --- Public API ---
def run_pipeline(bug_trace: str, user_review: Optional[str] = None) -> TriageResult:
    """Run the full bug triage pipeline.

    Args:
        bug_trace: The bug trace text
        user_review: Optional user commentary providing extra context

    Returns:
        TriageResult with issue_summary, steps, severity, and team
    """
    logger.info("=== Pipeline Started ===")

    initial_state = {
        "bug_trace": bug_trace,
        "user_review": user_review or "No user review provided",
    }

    final_state = pipeline.invoke(initial_state)

    triage_raw = final_state.get("triage_result")
    extraction_raw = final_state.get("extraction_result")

    if triage_raw is None or extraction_raw is None:
        logger.error("Pipeline completed but missing extraction or triage result")
        return TriageResult(
            issue_summary="Pipeline error: missing result",
            steps_to_reproduce=["Error"],
            technical_details= "Not provide", # type: ignore
            severity="Unknown",
            suggested_owner="Unknown"
        )

    # Merge into the final TriageResult
    result = TriageResult(
        issue_summary=extraction_raw.issue_summary,
        steps_to_reproduce=extraction_raw.steps_to_reproduce,
        technical_details=extraction_raw.technical_details,
        severity=triage_raw.severity,
        suggested_owner=triage_raw.suggested_owner
    )

    logger.info("=== Pipeline Complete ===\n")
    return result
