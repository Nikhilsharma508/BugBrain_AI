"""
src/duplicate_detection/vector_store.py — FAISS / ChromaDB Operations
----------------------------------------------------------------------
WHAT IT CAN DO (when implemented):
    - Create and load FAISS indexes (file-based, fast, zero setup)
    - Create and load ChromaDB collections (persistent, metadata support)
    - Add new report embeddings to the store
    - Search for top-K similar reports by vector similarity
    - Save/load index to/from data/vector_store/
    - Auto-create index on first run (handles empty store gracefully)

CONNECTS TO:
    - similarity.py uses search() to find similar reports
    - embeddings.py provides the vectors to store
    - scripts/build_vector_index.py builds the initial index from CSV
    - config/settings.py provides vector_store_type and vector_store_path
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv

from src.duplicate_detection.vector_store import get_vector_store
from src.telemetry.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.85"))

def search_similar_reports(query_text: str, top_k: int = 4, threshold: float = SIMILARITY_THRESHOLD) -> List[Dict[str, Any]]:
    """
    Searches for similar reports in the vector store using the query text.
    Returns matched reports that are above the certainty threshold.
    """
    try:
        vector_store = get_vector_store()
        
        # FAISS search_with_score returns (Document, score) where score is L2 distance typically.
        # But we can use similarity_search_with_relevance_scores to get a score between 0 and 1.
        results = vector_store.similarity_search_with_relevance_scores(query_text, k=top_k)
        
        matches = []
        for doc, score in results:
            if doc.metadata.get("id") == "init":
                continue # skip the dummy init document
                
            # Filter based on threshold
            if score >= threshold:
                matches.append({
                    "id": doc.metadata.get("id", "Unknown"),
                    "summary": doc.metadata.get("issue_summary", ""),
                    "steps": doc.metadata.get("steps", ""),
                    "severity": doc.metadata.get("severity", ""),
                    "team": doc.metadata.get("team", ""),
                    "similarity_score": score
                })
                
        return matches
    except Exception as e:
        logger.error(f"Failed to search for similar reports: {e}")
        return []
