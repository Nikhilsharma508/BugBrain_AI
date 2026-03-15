# `src/ui/` — Streamlit Application

## Purpose

Contains the full Streamlit web interface for the AI Bug Triage System.

## Structure

```
ui/
├── app.py              # Main entry point (run this)
├── pages/
│   ├── submit_report.py    # Bug report input + results
│   └── triage_dashboard.py # Metrics + history dashboard
└── components/
    ├── report_card.py      # Result card widget
    └── severity_badge.py   # Colour-coded severity pill
```

## Running

```bash
streamlit run src/ui/app.py
# or
make run-ui
```
