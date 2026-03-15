# src/config/settings.py — Project Settings
#
# PURPOSE:
#   Centralised settings class using Pydantic BaseSettings.
#   Reads all configuration from environment variables and .env file.
#   Every module in the project imports settings from here instead of
#   reading os.environ directly.
#
# USAGE:
#   from src.config import settings
#   api_key = settings.openai_api_key
#
# TODO:
#   - Define all fields with types, defaults, and descriptions
#   - Add model_config to read from .env file
#   - Add validation for required fields (e.g., OPENAI_API_KEY)

from pydantic_settings import BaseSettings
