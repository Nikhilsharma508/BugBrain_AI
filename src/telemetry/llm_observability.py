# src/telemetry/llm_observability.py — LangSmith / LangFuse Integration
#
# PURPOSE:
#   Provides production-grade LLM observability by integrating with
#   LangSmith (by LangChain) or LangFuse (open-source alternative).
#   Traces every LLM call with full input/output, token counts,
#   latency, and error details — viewable in a web dashboard.
#
# WHAT IT GIVES YOU:
#   - Full trace of every LLM call (prompt in → response out)
#   - Token usage breakdown per call and per session
#   - Latency histograms and P95/P99 percentiles
#   - Error rate monitoring and alerting
#   - Prompt versioning and A/B testing support
#   - Cost attribution per user/session/feature
#
# APPROACH:
#   LangSmith: Set env vars and LangChain auto-traces everything.
#   LangFuse: Use the LangFuse callback handler with LangChain.
#
# SETUP (LangSmith):
#   1. Sign up at https://smith.langchain.com
#   2. Create a project
#   3. Add to .env:
#      LANGCHAIN_TRACING_V2=true
#      LANGCHAIN_API_KEY=ls-your-key-here
#      LANGCHAIN_PROJECT=ai-bug-triage
#
# SETUP (LangFuse — open-source alternative):
#   1. Self-host or use https://cloud.langfuse.com
#   2. Add to .env:
#      LANGFUSE_PUBLIC_KEY=pk-your-key
#      LANGFUSE_SECRET_KEY=sk-your-key
#      LANGFUSE_HOST=https://cloud.langfuse.com
#
# KEY FUNCTIONS (planned):
#   - get_langsmith_callback() → Returns LangSmith callback handler
#   - get_langfuse_callback() → Returns LangFuse callback handler
#   - get_observability_callbacks() → Auto-selects based on env config
#
# USAGE:
#   from src.telemetry.llm_observability import get_observability_callbacks
#
#   callbacks = get_observability_callbacks()
#   llm = ChatOpenAI(model="gpt-4o-mini", callbacks=callbacks)
#   # All calls are now traced automatically in the dashboard
#
# TODO:
#   - Implement get_langsmith_callback() (auto-enabled via env vars)
#   - Implement get_langfuse_callback() using langfuse SDK
#   - Implement get_observability_callbacks() factory function
#   - Add graceful fallback if neither is configured (no-op)
#   - Add session/user tagging for multi-tenant tracing

from typing import Optional, List
import os

# --- LangSmith (auto-enabled by LangChain when env vars are set) ---
# Install:  pip install langsmith
# Env vars: LANGCHAIN_TRACING_V2=true, LANGCHAIN_API_KEY=..., LANGCHAIN_PROJECT=...
try:
    from langchain_core.callbacks import BaseCallbackHandler
    from langchain.callbacks.tracers import LangChainTracer
    _LANGSMITH_AVAILABLE = True
except ImportError:
    _LANGSMITH_AVAILABLE = False

# --- LangFuse (open-source alternative) ---
# Install:  pip install langfuse
# Env vars: LANGFUSE_PUBLIC_KEY=..., LANGFUSE_SECRET_KEY=..., LANGFUSE_HOST=...
try:
    from langfuse.callback import CallbackHandler as LangFuseCallbackHandler
    _LANGFUSE_AVAILABLE = True
except ImportError:
    _LANGFUSE_AVAILABLE = False

