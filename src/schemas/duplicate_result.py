# src/schemas/duplicate_result.py — Duplicate Detection Result Model
#
# PURPOSE:
#   Defines the Pydantic model for duplicate detection results.
#   Returned by the duplicate_detection module after comparing a new
#   report against existing tickets in the vector store.
#
# FIELDS (planned):
#   - is_duplicate: bool — Whether a likely duplicate was found
#   - similarity_score: float — Cosine similarity score (0.0 to 1.0)
#   - matched_report_id: Optional[str] — ID of the matching report
#   - matched_summary: Optional[str] — Summary of the matched report
#   - confidence: str — "high", "medium", "low"
#
# TODO:
#   - Define the DuplicateMatch Pydantic model
#   - Add threshold-based classification logic

from pydantic import BaseModel
from typing import Optional
