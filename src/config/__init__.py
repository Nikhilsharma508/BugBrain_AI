# src/config — Centralised Configuration
#
# This module provides a single source of truth for all project settings.
# It reads environment variables from .env using Pydantic BaseSettings.
#
# Exports:
#   - settings: The global Settings instance used throughout the project.

from src.config.settings import Settings

settings = Settings()

__all__ = ["settings", "Settings"]
