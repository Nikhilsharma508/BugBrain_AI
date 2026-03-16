"""
src/schemas/duplicate_result.py — Duplicate Detection Result Model
-------------------------------------------------------------------
PURPOSE:
    Defines the output model for the duplicate detection step.
    This is a stub for now — implementation comes when the
    duplicate_detection/ module is built.

HOW DUPLICATE DETECTION WILL WORK:
    1. Take the issue_summary from TriageResult
    2. Generate an embedding vector using OpenAI/HuggingFace embeddings
    3. Search the FAISS/ChromaDB vector store for top-K similar reports
    4. If the top match has similarity_score > threshold (default 0.85):
       → Flag as duplicate, return matched_report_id
    5. If no match exceeds threshold:
       → Not a duplicate, add this report's embedding to the store

EXTENSIBILITY:
    - Can add confidence scoring
    - Can return multiple potential matches for user review
    - Can use different similarity metrics (cosine, L2, dot product)

CONNECTS TO:
    - duplicate_detection/similarity.py will produce DuplicateMatch
    - orchestrator.py can insert a duplicate_check node between extract and triage
"""

from pydantic import BaseModel, Field
from typing import Optional


class DuplicateMatch(BaseModel):
    """Result of checking if a bug report is a duplicate."""

    is_duplicate: bool = Field(
        default=False,
        description="Whether this report matches an existing one",
    )
    similarity_score: float = Field(
        default=0.0,
        description="Cosine similarity score (0.0 to 1.0)",
    )
    matched_report_id: Optional[str] = Field(
        default=None,
        description="ID of the matching report, if duplicate",
    )
