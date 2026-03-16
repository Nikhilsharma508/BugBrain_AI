"""
src/config/settings.py — Centralised Configuration
----------------------------------------------------
PURPOSE:
    Single source of truth for all project settings.
    Reads from the root-level .env file using Pydantic BaseSettings.

CAPABILITIES:
    - Auto-loads all environment variables from .env
    - Type validation (wrong types raise clear errors at startup)
    - Default values for optional settings
    - Singleton pattern — import `settings` from anywhere

EXTENSIBILITY:
    - Add new env vars here → they're instantly available everywhere
    - Supports .env overrides, system env vars, and defaults
    - Can be extended with validators for custom logic

USAGE:
    from src.config.settings import settings
    print(settings.llm_model_name)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """All project configuration, loaded from .env at the project root."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignore env vars not listed here
    )

    # --- API Keys ---
    openai_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    openrouter_api_key: Optional[str] = None

    # --- LLM Configuration ---
    llm_model_name: str = "llama3-groq-tool-use:latest"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 2048

    # --- Embedding Model ---
    embedding_model_name: str = "text-embedding-3-small"

    # --- Vector Store ---
    vector_store_type: str = "faiss"
    vector_store_path: str = "data/vector_store"

    # --- Duplicate Detection ---
    similarity_threshold: float = 0.85

    # --- Logging ---
    log_level: str = "INFO"
    log_file_path: str = "data/temp/app.log"

    # --- Streamlit ---
    streamlit_port: int = 8501

    # --- LangSmith ---
    langchain_tracing_v2: Optional[str] = None
    langchain_api_key: Optional[str] = None
    langchain_project: Optional[str] = None


# Singleton — import this everywhere
settings = Settings()
