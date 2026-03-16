"""
src/duplicate_detection/similarity.py — Duplicate Check API
-------------------------------------------------------------
WHAT IT CAN DO (when implemented):
    - Check if a new bug report is a duplicate of an existing one
    - Return similarity score, confidence, and matched report ID
    - Configurable threshold from settings (default 0.85)
    - Return multiple potential matches for human review

HOW TO USE (after implementation):
    from src.duplicate_detection.similarity import check_duplicate
    result = check_duplicate("NullPointerException in UserService.login()")
    if result.is_duplicate:
        print(f"Duplicate of report {result.matched_report_id}")

CONNECTS TO:
    - Uses embeddings.py to vectorise the input
    - Uses vector_store.py to search for similar reports
    - Returns schemas/duplicate_result.DuplicateMatch
    - Can be added as a LangGraph node in orchestrator.py
"""
