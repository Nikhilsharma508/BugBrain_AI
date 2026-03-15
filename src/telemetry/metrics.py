# src/telemetry/metrics.py — Latency, Token Usage & Cost Tracking
#
# PURPOSE:
#   Tracks operational metrics for every pipeline invocation:
#     - End-to-end latency (seconds)
#     - LLM token usage (prompt tokens, completion tokens)
#     - Estimated cost in USD (based on model pricing)
#     - Error counts by type
#
# APPROACH:
#   Uses LangChain's get_openai_callback() to capture token usage,
#   and Python's time module for latency measurement.
#   Metrics are logged to a JSON Lines file for dashboard consumption.
#
# KEY CLASS:
#   MetricsTracker — with methods like:
#     - start_timer() → Start latency measurement
#     - stop_timer() → Stop and record latency
#     - record_tokens(prompt_tokens, completion_tokens, cost) → Log token usage
#     - get_summary() → Return aggregated stats
#     - export_to_jsonl(filepath) → Write metrics to JSON Lines file
#
# USED BY:
#   - Orchestrator (wraps each pipeline run)
#   - Streamlit dashboard (reads the JSONL file for display)
#
# TODO:
#   - Implement MetricsTracker class
#   - Add per-model pricing lookup table
#   - Add rolling window statistics (last 100 requests)

import time
import json
from typing import Optional
