# `src/telemetry/` — Internal Monitoring & Audit

## Purpose

Dedicated module for logging the project's **own internal operations** — not the bug reports themselves, but how the system performs while processing them.

## What It Tracks

| Metric | Where | Why |
|--------|-------|-----|
| Structured logs | Console + `data/temp/app.log` | Debug issues, trace pipeline flow |
| API latency | `data/temp/metrics.jsonl` | Monitor performance per request |
| Token usage | `data/temp/metrics.jsonl` | Track LLM consumption |
| Cost (USD) | `data/temp/metrics.jsonl` | Estimate spend for 100 queries |
| Error counts | `data/temp/metrics.jsonl` | Alert on failure spikes |
| Audit trail | `data/temp/audit.jsonl` | Full lifecycle log per request |

## Files

| File | Description |
|------|-------------|
| `__init__.py` | Exports: `setup_logger`, `MetricsTracker`, `AuditTrail`, `get_observability_callbacks` |
| `logger.py` | Structured Python logging setup (console + file) |
| `metrics.py` | Latency, token usage, and cost tracking |
| `audit_trail.py` | Per-request audit log writer |
| `llm_observability.py` | LangSmith / LangFuse integration for production LLM tracing |

## Usage

```python
from src.telemetry import setup_logger, MetricsTracker

logger = setup_logger(__name__)
tracker = MetricsTracker()

tracker.start_timer()
# ... run pipeline ...
tracker.stop_timer()
tracker.record_tokens(prompt_tokens=1200, completion_tokens=350, cost=0.0058)
```
