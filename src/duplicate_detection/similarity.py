"""
src/duplicate_detection/similarity.py — FAISS / ChromaDB Operations
----------------------------------------------------------------------
WHAT IT CAN DO:
    - Add new report embeddings to the store
    - Search for top-K similar reports by vector similarity utilizing Strategies
    - Save/load index to/from data/vector_store/
    - Auto-create index on first run (handles empty store gracefully)

CONNECTS TO:
    - orchestrator.py uses search_similar_reports to find duplicates
    - embeddings.py provides the vectors to store
    - config/settings.py provides vector_store_type and vector_store_path
"""

import os
import warnings
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

# Suppress LangChain relevance score warnings
warnings.filterwarnings("ignore", category=UserWarning)

from langchain_core.documents import Document

from src.duplicate_detection.vector_store import get_vector_store
from src.telemetry.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

EMBEDDING_SIMILARITY_THRESHOLD = float(
    os.getenv("EMBEDDING_SIMILARITY_THRESHOLD", "0.85")
)  # Default to 0.85, convert to float


def get_scores_for_docs(
    query_text: str,
    docs: List[Document],
    vector_store,
    top_k_for_scores: int = 100,
) -> List[Tuple[Document, float]]:
    """Helper to attach numeric scores to docs retrieved by non-scoring methods (MMR, MultiQuery)."""
    # Fetch a wider net to find the standard cosine score of our docs
    scored_results = vector_store.similarity_search_with_relevance_scores(
        query_text, k=top_k_for_scores
    )
    score_map = {
        str(d.metadata.get("id")): s
        for d, s in scored_results
        if d.metadata.get("id") != "init"
    }

    results_with_scores = []
    for doc in docs:
        doc_id = str(doc.metadata.get("id"))
        if doc_id == "init":
            continue
        # Default to 0.0 if the doc didn't appear in the top N (indicates low similarity)
        score = score_map.get(doc_id, 0.0)
        results_with_scores.append((doc, score))
    return results_with_scores


class RetrievalStrategy(ABC):
    @abstractmethod
    def search(
        self, query_text: str, top_k: int, threshold: float, vector_store
    ) -> List[Dict[str, Any]]:
        pass

    def _format_results(
        self, results: List[Tuple[Document, float]], threshold: float
    ) -> List[Dict[str, Any]]:
        matches = []
        for doc, score in results:
            if str(doc.metadata.get("id")) == "init":
                continue

            # Filter based on threshold
            if score >= threshold:
                matches.append(
                    {
                        "id": doc.metadata.get("id", "Unknown"),
                        "summary": doc.metadata.get("issue_summary", ""),
                        "steps": doc.metadata.get("steps", ""),
                        "severity": doc.metadata.get("severity", ""),
                        "team": doc.metadata.get("team", ""),
                        "similarity_score": score,
                    }
                )
        return matches


class CosineStrategy(RetrievalStrategy):
    """Standard L2/Cosine similarity search."""

    def search(
        self, query_text: str, top_k: int, threshold: float, vector_store
    ) -> List[Dict[str, Any]]:
        logger.info(f"Using CosineStrategy for search.")
        results = vector_store.similarity_search_with_relevance_scores(
            query_text, k=top_k
        )
        return self._format_results(results, threshold)


class MMRStrategy(RetrievalStrategy):
    """Maximal Marginal Relevance to balance relevance and diversity."""

    def search(
        self, query_text: str, top_k: int, threshold: float, vector_store
    ) -> List[Dict[str, Any]]:
        fetch_k = int(os.getenv("MMR_FETCH_K", "20"))
        lambda_mult = float(os.getenv("MMR_LAMBDA_MULT", "0.7"))
        logger.info(
            f"Using MMRStrategy for search. fetch_k={fetch_k}, lambda_mult={lambda_mult}"
        )

        docs = vector_store.max_marginal_relevance_search(
            query_text, k=top_k, fetch_k=fetch_k, lambda_mult=lambda_mult
        )
        scored = get_scores_for_docs(query_text, docs, vector_store, top_k_for_scores=max(100, fetch_k * 2))
        scored.sort(key=lambda x: x[1], reverse=True)
        return self._format_results(scored, threshold)


class MultiQueryStrategy(RetrievalStrategy):
    """Generates multiple queries using an LLM to improve recall across varied phrasings."""

    def search(
        self, query_text: str, top_k: int, threshold: float, vector_store
    ) -> List[Dict[str, Any]]:
        logger.info(f"Using MultiQueryStrategy for search.")
        from src.agents.agent import LLMManager
        from langchain_core.prompts import PromptTemplate

        llm = LLMManager().get_client()
        prompt = PromptTemplate(
            input_variables=["query"],
            template="You are an AI assistant. Generate 3 different versions of the following bug report summary "
            "to retrieve relevant documents from a vector database. Provide these alternative queries separated by newlines.\n"
            "Original query: {query}",
        )
        chain = prompt | llm
        
        try:
            res = chain.invoke({"query": query_text})
            text_res = res.content if hasattr(res, "content") else str(res)
            queries = [q.strip() for q in text_res.split("\n") if q.strip()]
        except Exception as e:
            logger.error(f"Failed to generate multiple queries: {e}")
            queries = []

        # Always include the original query
        queries.insert(0, query_text)

        # Collect results from all queries
        unique_docs = {}
        for q in queries:
            # We use a wider k for internal search then deduplicate
            results = vector_store.similarity_search_with_relevance_scores(q, k=top_k * 2)
            for doc, _ in results:
                doc_id = str(doc.metadata.get("id"))
                if doc_id not in unique_docs:
                    unique_docs[doc_id] = doc

        docs = list(unique_docs.values())
        scored = get_scores_for_docs(query_text, docs, vector_store, top_k_for_scores=100)
        scored.sort(key=lambda x: x[1], reverse=True)
        return self._format_results(scored[:top_k], threshold)


class ContextualStrategy(RetrievalStrategy):
    """Rewrites the query using an LLM to add broader technical context before searching."""

    def search(
        self, query_text: str, top_k: int, threshold: float, vector_store
    ) -> List[Dict[str, Any]]:
        from langchain_core.prompts import PromptTemplate
        from src.agents.agent import LLMManager

        llm = LLMManager().get_client()
        prompt = PromptTemplate(
            input_variables=["query"],
            template="You are a senior engineer. Rewrite this bug report to include broader technical context "
            "and standard development terminology that might be used to describe this issue in a codebase "
            "to help find similar previous bug reports. Keep it relatively concise but rich in keywords.\n\n"
            "Original Bug Report:\n{query}\n\nRewritten Bug Report Context:",
        )
        chain = prompt | llm
        try:
            contextual_query_msg = chain.invoke({"query": query_text})
            contextual_query = (
                contextual_query_msg.content
                if hasattr(contextual_query_msg, "content")
                else str(contextual_query_msg)
            )
            logger.debug(f"Contextually rewritten query: {contextual_query}")
        except Exception as e:
            logger.error(f"Failed to contextualize query: {e}. Falling back to original.")
            contextual_query = query_text

        # Use the enriched query to find candidates
        results = vector_store.similarity_search_with_relevance_scores(
            contextual_query, k=top_k
        )
        
        # Score candidates against the ORIGINAL query to keep thresholds stable
        docs = [d for d, _ in results]
        
        scored = get_scores_for_docs(query_text, docs, vector_store, top_k_for_scores=100)
        scored.sort(key=lambda x: x[1], reverse=True)
        return self._format_results(scored[:top_k], threshold)


def search_similar_reports(
    query_text: str, top_k: int = 4, threshold: float = EMBEDDING_SIMILARITY_THRESHOLD
) -> List[Dict[str, Any]]:
    """
    Searches for similar reports in the vector store using the configured strategy.
    Returns matched reports that are above the certainty threshold.
    """
    try:
        vector_store = get_vector_store()
        if not vector_store:
            logger.error("Vector store could not be initialized.")
            return []

        strategy_name = os.getenv("RETRIEVAL_STRATEGY", "cosine").lower()
        strategies = {
            "cosine": CosineStrategy(),
            "mmr": MMRStrategy(),
            "multiquery": MultiQueryStrategy(),
            "contextual": ContextualStrategy(),
        }

        strategy = strategies.get(strategy_name, CosineStrategy())
        return strategy.search(query_text, top_k, threshold, vector_store)
        
    except Exception as e:
        logger.error(f"Failed to search for similar reports using {os.getenv('RETRIEVAL_STRATEGY')}: {e}")
        return []
