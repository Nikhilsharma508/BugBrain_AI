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
from src.duplicate_detection.similarity import search_similar_reports
from src.telemetry.logger import get_logger
import json

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
    similar_reports: list[dict]

# --- Node Functions ---
def preprocess_node(state: dict) -> dict:
    """LangGraph node: run preprocessing pipeline."""
    bug_trace = state.get("bug_trace", "")
    logger.info("Running preprocessing...")

    result = run_preprocessing(bug_trace)

    return {
        "cleaned_text": result["cleaned_text"]
    }


def duplicate_detection_node(state: dict) -> dict:
    """LangGraph node: search for similar reports using the vector store."""
    logger.info("Running duplicate detection node...")
    user_review = state.get("user_review", "")
    extraction = state.get("extraction_result")
    
    if not extraction:
        return {"similar_reports": []}
        
    tech_details_dict = extraction.technical_details.model_dump() if hasattr(extraction.technical_details, 'model_dump') else extraction.technical_details
    combined_text = f"""
    User Review: {user_review}
    Issue Summary: {extraction.issue_summary}
    Steps to Reproduce: {', '.join(extraction.steps_to_reproduce)}
    User Impact: {extraction.user_impact_assessment}
    Technical Details: {json.dumps(tech_details_dict)}
    """
    
    similar_reports = search_similar_reports(combined_text)
    return {"similar_reports": similar_reports}


# --- Build the Graph ---
def build_pipeline() -> StateGraph:
    """Build and compile the LangGraph pipeline."""
    graph = StateGraph(PipelineState)

    # Add nodes
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("extract", run_extraction)
    graph.add_node("duplicate_detection", duplicate_detection_node)
    graph.add_node("triage", run_triage)

    # Define edges: START → preprocess → extract → duplicate_detection → triage → END
    graph.add_edge(START, "preprocess")
    graph.add_edge("preprocess", "extract")
    graph.add_edge("extract", "duplicate_detection")
    graph.add_edge("duplicate_detection", "triage")
    graph.add_edge("triage", END)

    return graph.compile()


# Compile once at import
pipeline = build_pipeline()


# --- Public API ---
def run_pipeline(bug_trace: str, user_review: Optional[str] = None):
    """Run the full bug triage pipeline and stream results.

    Args:
        bug_trace: The bug trace text
        user_review: Optional user commentary providing extra context

    Yields:
        Dict: Intermediate states from LangGraph execution, ending with 
              a final dictionary containing 'final_triage_result': TriageResult.
    """
    logger.info("=== Pipeline Started ===")

    initial_state = {
        "bug_trace": bug_trace,
        "user_review": user_review or "No user review provided",
    }

    final_state_snapshot = {}
    
    # We use pipeline.stream instead of invoke
    for step_output in pipeline.stream(initial_state):
        # We merge into snapshot so we know the cumulative state
        for node_name, node_state in step_output.items():
            final_state_snapshot.update(node_state)
            
            # Yield the node's name and the combined current state to the caller (e.g. Streamlit UI)
            yield {
                "node_name": node_name,
                "current_state": final_state_snapshot
            }

    triage_raw = final_state_snapshot.get("triage_result")
    extraction_raw = final_state_snapshot.get("extraction_result")

    if triage_raw is None or extraction_raw is None:
        logger.error("Pipeline completed but missing extraction or triage result")
        yield {
            "node_name": "error",
            "final_triage_result": TriageResult(
                issue_summary="Pipeline error: missing result",
                steps_to_reproduce=["Error"],
                technical_details= "Not provide", # type: ignore
                severity="Unknown",
                suggested_owner="Unknown"
            )
        }
        return

    # Merge into the final TriageResult
    result = TriageResult(
        issue_summary=extraction_raw.issue_summary,
        steps_to_reproduce=extraction_raw.steps_to_reproduce,
        user_impact_assessment=extraction_raw.user_impact_assessment,
        technical_details=extraction_raw.technical_details,
        triage_reasoning=triage_raw.triage_reasoning,
        severity=triage_raw.severity,
        suggested_owner=triage_raw.suggested_owner,
    )
    
    logger.info("=== Pipeline Complete ===\n")
    yield {
        "node_name": "completed",
        "final_triage_result": result,
        "similar_reports": final_state_snapshot.get("similar_reports", []),
        "combined_text": final_state_snapshot.get("combined_text_for_search", "")
    }