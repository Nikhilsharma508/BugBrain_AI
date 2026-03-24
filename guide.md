# 📘 AI Bug Triage System — Complete Setup & Development Guide

# 4. Setting Up CI/CD with GitHub Actions - pending

CI/CD (Continuous Integration / Continuous Deployment) automatically runs your tests and checks every time you push code to GitHub.

- ✅ Tests run automatically before merging
- ✅ Linting catches style issues
- ✅ Broken code never reaches `main` branch

---

# 5. Cost Tracking — How We'll Estimate OpenAI Token Spend - pending

The submission requires: *"Cost estimation to process 100 user queries."*

### Our approach:

**Where:** `src/telemetry/metrics.py`

**How it works:**

1. **LangChain's built-in callback** tracks tokens per request:
   ```python
   from langchain_community.callbacks import get_openai_callback

   with get_openai_callback() as cb:
       result = run_pipeline(raw_report)
       # cb.total_tokens     → total tokens used
       # cb.total_cost       → cost in USD
       # cb.prompt_tokens    → input tokens
       # cb.completion_tokens → output tokens
   ```

2. **We log every request's cost** to a JSON Lines file:
   ```json
   {"timestamp": "2026-03-15T10:00:00", "report_id": "BUG-42", "prompt_tokens": 1200, "completion_tokens": 350, "total_cost_usd": 0.0058}
   ```


4. **For the submission**, we run the pipeline on sample data and compute:
   ```
   Average cost per query = Total spend / Number of queries
   Cost for 100 queries  = Average cost × 100
   ```

### Pricing reference (GPT-4o as of 2026):
| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|----------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |

---