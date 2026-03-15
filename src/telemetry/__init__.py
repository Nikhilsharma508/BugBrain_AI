# src/telemetry — Internal Monitoring & Audit
#
# This package handles all internal observability:
# structured logging, API latency tracking, token/cost metrics,
# and per-request audit trails.
#
# Exports:
#   - setup_logger: Configure structured Python logging
#   - MetricsTracker: Latency, token usage, error counters
#   - AuditTrail: Per-request audit log writer

from src.telemetry.logger import setup_logger
from src.telemetry.metrics import MetricsTracker
from src.telemetry.audit_trail import AuditTrail
from src.telemetry.llm_observability import get_observability_callbacks

__all__ = ["setup_logger", "MetricsTracker", "AuditTrail", "get_observability_callbacks"]
