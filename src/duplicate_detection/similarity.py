# src/duplicate_detection/similarity.py — New Report vs. Existing Comparison
#
# PURPOSE:
#   High-level API for checking if a new bug report is a duplicate.
#   Orchestrates the embedding + vector search + threshold check.
#
# KEY CLASS:
#   SimilarityChecker — with methods like:
#     - check_duplicate(new_report_text: str) → DuplicateMatch
#
# LOGIC:
#   1. Embed the new report's summary using EmbeddingManager
#   2. Search the vector store for top-K similar reports
#   3. If top result's similarity score > threshold → flag as duplicate
#   4. Return DuplicateMatch with score, matched ID, and confidence
#
# TODO:
#   - Implement check_duplicate() using EmbeddingManager + VectorStoreManager
#   - Make similarity threshold configurable from settings
#   - Return rich metadata about the matched report

from typing import Optional
