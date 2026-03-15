# 🐛 AI Bug Triage System

> Automate the ingestion of unstructured bug reports and produce standardised, clean technical briefs — ready for Jira / GitHub Issues.

## 🏗️ Architecture Overview

```
Raw Bug Report → Preprocessing (Regex/Noise Filter)
                    ↓
              Extraction Agent (LangChain → Structured JSON)
                    ↓
              Duplicate Detection (FAISS/ChromaDB RAG)
                    ↓
              Triage Agent (Severity + Team Assignment)
                    ↓
              Structured Output (JSON → Jira-ready)
```

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Signal-to-Noise Filtering** | Strips emotional language, memory dumps, and irrelevant context from bug reports |
| **Structured Extraction** | Converts raw text into standardised JSON (summary, steps, technical details) |
| **Duplicate Detection** | Uses vector embeddings + similarity search to flag potential duplicate tickets |
| **Auto-Severity Assignment** | Applies configurable policy rules (P1–P4) based on impact analysis |
| **Team Routing** | Suggests the responsible team (Frontend, Backend, Mobile, etc.) |
| **Internal Telemetry** | Logs latency, token usage, costs, and errors for every request |

## 🛠️ Tech Stack

- **UI**: Streamlit
- **AI Orchestration**: LangChain (Agents + Memory)
- **Vector Database**: FAISS / ChromaDB
- **Core Logic**: Python (Regex for log parsing)
- **Data Models**: Pydantic v2
- **Configuration**: YAML policy files + Pydantic BaseSettings
- **Monitoring**: Python `logging` + custom metrics

## 📁 Project Structure

```
├── src/                    # Production source code
│   ├── config/             # Settings and env config
│   ├── preprocessing/      # Log parsing and noise filtering
│   ├── schemas/            # Pydantic data models
│   ├── agents/             # LangChain agent definitions
│   ├── prompts/            # Prompt templates
│   ├── duplicate_detection/# RAG + vector similarity
│   ├── policies/           # Severity rules & team routing (YAML)
│   ├── telemetry/          # Logging, metrics, audit trail
│   └── ui/                 # Streamlit app (pages + components)
├── data/                   # Runtime data storage
├── tests/                  # Unit + integration tests
├── docs/                   # Architecture & API docs
├── scripts/                # Setup and utility scripts
└── notebooks/              # Exploration notebooks
```

## 🚀 Quick Start

```bash
# 1. Clone and enter the project
cd "UC20 - Bug Report Summarizer & Triage Assistant"

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 5. Run the Streamlit app
make run-ui
```

> 📘 **For a complete setup guide, see [guide.md](./guide.md)**

## 📋 Expected Output Format

```json
{
  "issue_summary": "Inconsistent 'Purchase' button failure on iPad/Safari",
  "steps_to_reproduce": [
    "Open app on iPad (v17.2)",
    "Add item to cart",
    "Navigate to Checkout",
    "Click 'Purchase' button multiple times"
  ],
  "technical_details": {
    "detected_error": "Timeout in API call /v1/transactions",
    "environment": "iOS Safari"
  },
  "severity": "P1 (Critical - Revenue Impacting)",
  "suggested_owner": "Payments-Backend-Team"
}
```

## 📄 License

This project is for educational and internal use.
