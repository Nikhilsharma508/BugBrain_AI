# `tests/` — Test Suite

## Purpose
Contains all automated tests for the AI Bug Triage System, organised into unit and integration tests.

## Structure

| Folder | Tests | Run with |
|--------|-------|----------|
| `unit/` | Isolated tests for individual functions/classes | `pytest tests/unit/` |
| `integration/` | End-to-end tests that involve multiple modules | `pytest tests/integration/` |

## Running Tests

```bash
# All tests
make test

# Unit tests only
make test-unit

# With verbose output
pytest tests/ -v -s
```
