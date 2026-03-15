# src/telemetry/audit_trail.py — Per-Request Audit Log Writer
#
# PURPOSE:
#   Creates an immutable audit log for every bug report processed.
#   Records the full lifecycle: input received → preprocessing →
#   extraction → duplicate check → triage → output delivered.
#
# FIELDS PER AUDIT ENTRY:
#   - request_id: str (UUID)
#   - timestamp: datetime
#   - input_hash: str (SHA-256 of raw input — for deduplication without storing PII)
#   - preprocessing_result: str (summary of what was filtered)
#   - extraction_result: dict (structured output)
#   - duplicate_check: dict (was it a duplicate? score?)
#   - triage_result: dict (severity, team)
#   - latency_ms: float
#   - tokens_used: int
#   - status: str ("success" | "error")
#   - error_message: Optional[str]
#
# KEY CLASS:
#   AuditTrail — with methods like:
#     - log_request(entry: dict) → Write one audit entry
#     - get_history(limit: int) → Read recent audit entries
#
# TODO:
#   - Implement AuditTrail class
#   - Write to JSON Lines file in data/temp/audit.jsonl
#   - Add request_id generation (UUID4)

import json
import uuid
from datetime import datetime
from typing import Optional
