"""
src/duplicate_detection/ — Vector Similarity & Duplicate Check
-----------------------------------------------------------------
PURPOSE:
    Detects if a new bug report is a duplicate of an existing one
    using vector embeddings and similarity search.

WHAT IT CAN DO:
    - Generate text embeddings via OpenAI or HuggingFace models
    - Store embeddings in FAISS (file-based) or ChromaDB (persistent)
    - Search for similar reports using cosine similarity
    - Flag duplicates when similarity score exceeds threshold
    - Return the matched report ID and confidence score

HOW IT WORKS (when implemented):
    1. Take the issue_summary from TriageResult
    2. Embed it using EmbeddingManager
    3. Search the vector store for top-K similar reports
    4. If top match score > 0.85 threshold → flag as duplicate
    5. Otherwise → add to the store as a new unique report

EXTENSIBILITY:
    - Can be added as a LangGraph node between "extract" and "triage"
    - Multiple similarity metrics (cosine, dot product, L2)
    - Batch processing for CSV ingestion
    - Confidence-based routing (auto-merge vs human review)

CONNECTS TO:
    - orchestrator.py can add a "duplicate_check" node
    - schemas/duplicate_result.py defines the DuplicateMatch output
    - config/settings.py provides similarity_threshold and vector_store_path
"""
