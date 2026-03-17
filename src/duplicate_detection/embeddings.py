import os
from typing import List
from dotenv import load_dotenv

from langchain_ollama import OllamaEmbeddings
from src.telemetry.logger import get_logger

logger = get_logger(__name__)

# Load environment variables
load_dotenv()

_embedding_model = None

def get_embedding_model() -> OllamaEmbeddings:
    """Returns a singleton instance of the OllamaEmbeddings model."""
    global _embedding_model
    if _embedding_model is None:
        model_name = os.getenv("OLLAMA_EMBEDDING_MODEL", "qwen3-embedding:0.6b")
        logger.info(f"Initializing embedding model: {model_name}")
        _embedding_model = OllamaEmbeddings(model=model_name)
    return _embedding_model

def get_embeddings(text: str) -> List[float]:
    """Generates an embedding for a single text string."""
    try:
        model = get_embedding_model()
        return model.embed_query(text)
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        raise

def get_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """Generates embeddings for a batch of text strings."""
    try:
        model = get_embedding_model()
        return model.embed_documents(texts)
    except Exception as e:
        logger.error(f"Error generating batch embeddings: {e}")
        raise
