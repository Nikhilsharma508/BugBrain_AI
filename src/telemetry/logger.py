"""
src/telemetry/logger.py — Structured Logging Setup
----------------------------------------------------
PURPOSE:
    Provides consistent, structured logging across the entire project.
    Every module calls get_logger(__name__) to get a configured logger.

WHAT IT DOES NOW:
    - Console output with timestamp, level, module name, and message
    - File output (RotatingFileHandler) saved to data/temp/app.log
    - Configurable log level from .env (LOG_LEVEL)

CAPABILITIES (can be extended later):
    - JSON formatter: structured logs for machine parsing (ELK, Datadog)
    - Coloured output: different colors for ERROR vs INFO vs DEBUG
    - Context injection: add request_id, session_id to every log line
    - Remote logging: send to CloudWatch, GCP Logging, etc.
    - Performance logging: auto-log function execution time

CONNECTS TO:
    - Every module imports: from src.telemetry.logger import get_logger
    - extraction_agent.py, triage_agent.py, orchestrator.py all use it
    - Reads LOG_LEVEL and LOG_FILE_PATH directly from .env

USAGE:
    from src.telemetry.logger import get_logger
    logger = get_logger(__name__)
    logger.info("Processing bug report", extra={"report_id": 42})
"""

import logging
import sys
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

# Cache loggers to avoid duplicate handlers
_loggers: dict[str, logging.Logger] = {}


def get_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """Get a configured logger instance.

    Args:
        name: Logger name (typically __name__)
        level: Override log level. If None, reads from settings.

    Returns:
        Configured logging.Logger instance
    """
    if name in _loggers:
        return _loggers[name]

    from dotenv import load_dotenv

    load_dotenv()
    log_level = level or os.getenv("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(numeric_level)

    # Only add handlers if none exist (prevents duplicate output)
    if not logger.handlers:
        # Common formatter
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # 1. Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # 2. File Handler (Rotating)
        log_file_path = os.getenv("LOG_FILE_PATH", "data/temp/app.log")
        log_file = Path(log_file_path)
        try:
            # Ensure log directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5 * 1024 * 1024,  # 5MB
                backupCount=5,
                encoding="utf-8",
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # Fallback if file logging fails (e.g. permission error)
            logger.error(f"Failed to set up file logging at {log_file}: {e}")

    _loggers[name] = logger
    return logger
