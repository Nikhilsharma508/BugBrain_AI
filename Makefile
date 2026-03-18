# ============================================================
# AI Bug Triage System — Makefile
# Common development commands
# ============================================================

.PHONY: install test run-ui clean help

# Default target
help:
	@echo ""
	@echo "  AI Bug Triage System — Available Commands"
	@echo "  ──────────────────────────────────────────"
	@echo "  make install     Install project + dev dependencies"
	@echo "  make run-ui      Start Streamlit app"
	@echo "  make clean       Remove caches and temp files"
	@echo "  make test        Run all tests"
	@echo "  make test-unit   Run unit tests only"
	@echo "  make load-data   Load CSV data and build vector index"
	@echo ""

install:
	pip install -e ".[dev]"

# Test targets
test:
	pytest tests/ -v --tb=short

test-unit:
	pytest tests/unit/ -v --tb=short

run-ui:
	streamlit run src/ui/app.py --server.port 8501

load-data:
	python scripts/load_csv_data.py
	python scripts/build_vector_index.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf data/temp/* 2>/dev/null || true
	@echo "Cleaned!"
