# src/telemetry/logger.py — Structured Python Logging Setup
#
# PURPOSE:
#   Configures Python's built-in logging module for the entire project.
#   Provides structured, consistent log output to both console and file.
#
# FEATURES (planned):
#   - JSON-formatted log lines for machine readability
#   - Configurable log level from settings (LOG_LEVEL env var)
#   - File handler writing to data/temp/app.log
#   - Console handler with colour-coded output
#
# KEY FUNCTION:
#   setup_logger(name: str) → logging.Logger
#
# USAGE:
#   from src.telemetry import setup_logger
#   logger = setup_logger(__name__)
#   logger.info("Processing bug report", extra={"report_id": 42})
#
# TODO:
#   - Implement setup_logger with console + file handlers
#   - Add JSON formatter for structured logging
#   - Read log level from src/config/settings

import logging
from typing import Optional
