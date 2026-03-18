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
from pathlib import Path
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import uuid

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from src.duplicate_detection.embeddings import get_embedding_model
from src.telemetry.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

_vector_store = None
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "Data/vector_store")


def get_vector_store() -> FAISS:
    """Returns a singleton instance of the FAISS vector store. Loads from disk if exists, else creates new."""
    global _vector_store
    if _vector_store is None:
        model = get_embedding_model()
        path = Path(VECTOR_STORE_PATH)

        if path.exists() and (path / "index.faiss").exists():
            logger.info(f"Loading existing FAISS index from {VECTOR_STORE_PATH}")
            try:
                # Add allow_dangerous_deserialization=True explicitly for loading local indices safely
                _vector_store = FAISS.load_local(
                    str(path), model, allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.error(
                    f"Failed to load FAISS index: {e}. Reinitializing empty store."
                )
                _vector_store = None
        else:
            logger.info(
                "Initializing new empty FAISS index (will be populated on first text add)."
            )
            # Create a dummy element to initialize FAISS, we can delete it later,
            # or just wait to initialize it when adding the first texts.
            # Langchain FAISS from_texts requires at least one text.
            _vector_store = FAISS.from_texts(
                ["init"], model, metadatas=[{"id": "init"}]
            )
            # Save it so it's initialized
            os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
            _vector_store.save_local(VECTOR_STORE_PATH)

    return _vector_store


def get_indexed_ids() -> set:
    """Returns a set of all report IDs currently in the index (based on metadata 'id' field)."""
    try:
        vector_store = get_vector_store()
        docstore = vector_store.docstore

        indexed_ids = set()
        for doc_id, doc in docstore._dict.items():
            if "id" in doc.metadata and doc.metadata["id"] != "init":
                indexed_ids.add(str(doc.metadata["id"]))
        return indexed_ids
    except Exception as e:
        logger.error(f"Could not retrieve indexed IDs: {e}")
        return set()


def add_reports_to_index(texts: List[str], metadatas: List[Dict[str, Any]]):
    """Adds new reports to the vector store index and saves it to disk."""
    if not texts:
        return

    logger.info(f"Adding {len(texts)} reports to vector store.")
    try:
        vector_store = get_vector_store()
        vector_store.add_texts(texts=texts, metadatas=metadatas)
        # Save to disk
        vector_store.save_local(VECTOR_STORE_PATH)
        logger.info("Successfully added reports and saved to disk.")
    except Exception as e:
        logger.error(f"Failed to add reports to index: {e}")
        raise
