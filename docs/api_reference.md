# API Reference — AI Bug Triage System

## Core Entry Point

### `src.agents.orchestrator.run_pipeline(raw_text: str) → TriageResult`
The main function to process a bug report end-to-end.

---

## Preprocessing (`src.preprocessing`)

### `LogParser`
- `extract_stack_traces(raw_text: str) → List[str]`
- `extract_error_codes(raw_text: str) → List[str]`
- `parse(raw_text: str) → dict`

### `NoiseFilter`
- `filter(raw_text: str) → str`

### `TextCleaner`
- `clean(raw_text: str) → str`

---

## Schemas (`src.schemas`)

### `BugReport` — Input model
### `TriageResult` — Output JSON contract
### `DuplicateMatch` — Duplicate detection result

---

## Agents (`src.agents`)

### `ExtractionAgent`
- `extract(cleaned_text: str) → TriageResult`

### `TriageAgent`
- `classify(extraction_result: TriageResult) → TriageResult`

---

## Duplicate Detection (`src.duplicate_detection`)

### `SimilarityChecker`
- `check_duplicate(new_report_text: str) → DuplicateMatch`

---

## Telemetry (`src.telemetry`)

### `setup_logger(name: str) → logging.Logger`
### `MetricsTracker`
- `start_timer()` / `stop_timer()`
- `record_tokens(prompt_tokens, completion_tokens, cost)`
### `AuditTrail`
- `log_request(entry: dict)`
- `get_history(limit: int) → List[dict]`

---

> **Note:** This reference will be expanded as modules are implemented. See each module's README.md for detailed documentation.
