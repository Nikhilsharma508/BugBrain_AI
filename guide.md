# 📘 AI Bug Triage System — Complete Setup & Development Guide

---

# 1. Understanding `src/policies/` — Severity Rules in Simple Words - pending

**What is it?**
Think of `policies/` as a **rule book** written in plain English (YAML format) — not Python code.

**Why do we need it?**
Right now, the AI needs rules to decide:
- *"Is this bug critical (P1) or minor (P4)?"*
- *"Should this go to the Backend team or the Frontend team?"*

Instead of **hard-coding** these rules inside Python files (which means a developer must edit code every time a rule changes), we put them in a simple YAML file.

**Example — `severity_policy.yaml`:**
```yaml
severity_levels:
  P1_Critical:
    description: "System down, revenue impacting, or login blocked"
    conditions:
      - "affects more than 100 users"
      - "blocks login or checkout"
      - "causes data loss"

  P2_High:
    description: "Major feature broken but workaround exists"
    conditions:
      - "affects 10-100 users"
      - "core feature broken with workaround"

  P3_Medium:
    description: "Minor feature issue"
    conditions:
      - "affects 1-10 users"
      - "non-core feature broken"

  P4_Low:
    description: "Cosmetic or trivial"
    conditions:
      - "typo or visual glitch"
      - "affects 1 user with easy workaround"
```

**Who benefits?**
- A **Product Manager** can open this YAML file, change the rules (e.g., change "100 users" to "50 users"), and save — **no Python knowledge needed**.
- The Python code simply **reads** this file and passes the rules to the AI agent.

---

# 3. Adding FastAPI Later (Without Breaking Anything) - pending

**Short answer: Yes, absolutely!** The project is designed so FastAPI can be added later with **minimal changes** to existing files.

### Why it's easy:

The `orchestrator.py` in `src/agents/` is the central pipeline. It takes a raw bug report string and returns a structured result. Both Streamlit and FastAPI would call the **same** orchestrator.

### Steps to add FastAPI later:

1. **Create a new folder:** `src/api/`
2. **Add two files:**
   - `src/api/__init__.py`
   - `src/api/endpoints.py`

3. **Write the endpoint** (example):
   ```python
   from fastapi import FastAPI
   from src.agents.orchestrator import run_pipeline
   from src.schemas.triage_output import TriageResult

   app = FastAPI(title="Bug Triage API")

   @app.post("/triage", response_model=TriageResult)
   async def triage_bug(raw_report: str):
       result = run_pipeline(raw_report)
       return result
   ```

4. **Add `fastapi` and `uvicorn` to `pyproject.toml`:**
   ```toml
   dependencies = [
       # ... existing deps ...
       "fastapi>=0.100.0",
       "uvicorn>=0.20.0",
   ]
   ```

5. **Run:** `uvicorn src.api.endpoints:app --reload`

### What changes in existing files?
- **ZERO changes** to `src/agents/`, `src/preprocessing/`, `src/schemas/`, etc.
- You only **add** a new `src/api/` folder. The architecture is designed for this.

---

# 4. Setting Up CI/CD with GitHub Actions - pending

CI/CD (Continuous Integration / Continuous Deployment) automatically runs your tests and checks every time you push code to GitHub.

### Step-by-step:

**Step 1:** Create the workflow directory:
```bash
mkdir -p .github/workflows
```

**Step 2:** Create `.github/workflows/ci.yml`:
```yaml
name: CI Pipeline

# When to run: on every push and pull request to main
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      # 1. Check out the code
      - name: Checkout repository
        uses: actions/checkout@v4

      # 2. Set up Python
      - name: Set up Python 3.11
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      # 3. Cache pip dependencies (speeds up builds)
      - name: Cache pip
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      # 4. Install dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -e ".[dev]"

      # 5. Run unit tests
      - name: Run tests
        run: pytest tests/ -v --tb=short

      # 7. (Optional) Check types
      # - name: Type check with mypy
      #   run: mypy src/

  # Optional: Build check
  build:
    runs-on: ubuntu-latest
    needs: test  # Only runs if tests pass

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Build package
        run: |
          pip install build
          python -m build
```

**Step 3:** Push to GitHub:
```bash
git add .github/
git commit -m "Add CI/CD pipeline"
git push
```

**Step 4:** Check results:
- Go to your GitHub repo → **Actions** tab
- You'll see your pipeline running automatically on every push

### What does this give you?
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

3. **The Streamlit dashboard** reads this log and shows:
   - Average cost per query
   - Total spend so far
   - Projected cost for 100 queries

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

# 6. Initial Project Setup — Full Walkthrough - completed

Follow these steps **in order** after the project structure has been created.

## 6.1 Prerequisites

Make sure you have installed:
```bash
# Check Python version (need 3.10+)
python3 --version

# Check pip
pip3 --version

# Check git
git --version
```

If missing, install:
- **Python 3.11+**: https://www.python.org/downloads/
- **Git**: https://git-scm.com/downloads

## 6.2 Initialise Git Repository

```bash
# Navigate to the project folder
cd "/Users/nike/Documents/Data Science Work/Project/UC20 - Bug Report Summarizer & Triage Assistant"

# Initialise a new Git repository
git init

# Add the .gitignore first (already created for you)
git add .gitignore

# Make the first commit
git add .
git commit -m "Initial project structure: AI Bug Triage System"
```

## 6.3 Create a GitHub Repository (Optional but Recommended) - completed

```bash
# Option A: Using GitHub CLI (gh)
# Install: brew install gh
gh auth login
gh repo create "ai-bug-triage-system" --private --source=. --push

# Option B: Manual
# 1. Go to https://github.com/new
# 2. Create a new repo (private recommended)
# 3. Follow the instructions to push an existing repo:
git remote add origin https://github.com/YOUR_USERNAME/ai-bug-triage-system.git
git branch -M main
git push -u origin main
```

## 6.4 Create Virtual Environment - completed

```bash
# Create a virtual environment named .venv
python3 -m venv .venv

# Activate it
source .venv/bin/activate   # macOS / Linux

# Verify you're in the venv
which python
# Should show: .../UC20 - Bug Report Summarizer .../  .venv/bin/python
```

## 6.5 Install Dependencies

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Or use requirements.txt
pip install -r requirements.txt
```

## 6.6 Set Up Environment Variables

```bash
# Copy the template
cp .env.example .env

# Open and fill in your real values
nano .env   # or open in VS Code: code .env
```

**Required variables to fill in:**
```
OPENAI_API_KEY=sk-your-actual-key-here
LLM_MODEL_NAME=gpt-4o-mini        # or gpt-4o
```

## 6.7 Load Data into the Project

```bash
# Copy the existing CSV into the data pipeline
python scripts/load_csv_data.py

# Build the initial vector index (for duplicate detection)
python scripts/build_vector_index.py
```

## 6.8 Run the Streamlit App

```bash
# Using Make (recommended)
make run-ui

# Or directly
streamlit run src/ui/app.py
```

## 6.9 Run Tests

```bash
# Run all tests
make test

# Or directly
pytest tests/ -v

# Run only unit tests
pytest tests/unit/ -v
```

## 6.10 Commit Your Work Regularly

```bash
# Check status
git status

# Stage and commit
git add .
git commit -m "feat: implement preprocessing pipeline"

# Push to GitHub
git push
```

### Recommended Commit Message Prefixes:
| Prefix | Use for |
|--------|---------|
| `feat:` | New features |
| `fix:` | Bug fixes |
| `docs:` | Documentation changes |
| `refactor:` | Code restructuring |
| `test:` | Adding/updating tests |
| `chore:` | Config, dependencies, etc. |

---

# 7. Quick Reference — Common Commands

```bash
# ──────────────── Daily Development ────────────────
source .venv/bin/activate          # Activate venv
make run-ui                        # Start Streamlit
make test                          # Run tests
make run-ui                          # Start Streamlit (alternate)

# ──────────────── Git Workflow ────────────────
git add .
git commit -m "feat: your message"
git push

# ──────────────── Dependencies ────────────────
pip install some-package           # Install new package
pip freeze > requirements.txt      # Update requirements
pip install -e ".[dev]"            # Reinstall project

# ──────────────── Debugging ────────────────
streamlit run src/ui/app.py --logger.level=debug
pytest tests/ -v -s                # Verbose with print output
```

---

> **💡 Tip:** Bookmark this guide! Come back here whenever you need to remember a step. Each section is independent — you can jump to any section without reading the ones before it.


# 8. Two libraries are missing from 

pyproject.toml
 / 

requirements.txt
:

Library	Used in	Status
langsmith	

llm_observability.py
❌ Not in 

pyproject.toml
langfuse	

llm_observability.py
❌ Not in 

pyproject.toml

# 9 First of all set up uv
- install uv
> init uv

> uv add `library`

# 10: signals: dict not being used

# Automated Tests
Script Validation: Run python scripts/load_json_data.py. Verify that Data/processed correctly populates with new .json files corresponding to unindexed rows without throwing exceptions.
Vector Index Validation: Run python scripts/build_vector_index.py. Verify that Data/vector_store/index.faiss and index.pkl are generated/updated. Re-run the script to ensure it skips already indexed documents.


Manual Verification
UI Layout: Run streamlit run src/ui/app.py. Submit a new bug report. Wait for pipeline analysis. Visually verify the 3-column layout matches the screenshot.
Duplicate Search: Check the far-right column for "RAG Similarity Search". Ensure duplicates return plausible similarity scores.
Ready to Commit Workflow: Click "Ready to Commit". Verify that:
The CSV receives a new row.
A new JSON file appears in Data/processed/.
The vector store is updated (file modified time changes, or subsequent exact-match searches return 100% similarity).

# one problem is that, if give garbage data, it still give you something.
- I can improve on logging system, which is not just taking the INFO but other critical viewpoints (like warning, debug etc)
- More modularize - means some function create multiple times.
