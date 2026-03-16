"""
scripts/test_pipeline.py — End-to-End Pipeline Test
---------------------------------------------------
PURPOSE:
    Tests the complete AI Bug Triage pipeline from end-to-end.
    Loads a real bug report from the CSV, passes it through the
    orchestrator, and prints the extracted structured JSON.

USAGE:
    Run this script from the project root:
    $ python scripts/test_pipeline.py
"""

import sys
import pandas as pd
from pathlib import Path

# Add project root to PYTHONPATH so we can import src
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.agents.orchestrator import run_pipeline
from src.telemetry.logger import get_logger

logger = get_logger("test_pipeline")


def main():
    logger.info("Setting up pipeline test...")

    csv_path = project_root / "Data" / "bug_report.csv"
    if not csv_path.exists():
        logger.error(f"Could not find CSV at {csv_path}")
        return

    logger.info(f"Loading data from {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return

    if df.empty:
        logger.error("CSV is empty!")
        return

    # Let's grab the first real bug report from the dataset
    sample_row = df.iloc[0]
    bug_id = sample_row.get("Id", "Unknown")
    bug_trace = sample_row.get("Bug Details", "")
    
    # Check if 'User Review' column exists, otherwise default
    user_review = sample_row.get("User Review", "No user review provided") if "User Review" in df.columns else "No user review provided"

    # type of bug_trace and user_review should be string for the pipeline, ensure that
    # print(f"Type of bug_trace: {type(bug_trace)}, Type of user_review: {type(user_review)}") # Str , Str (result)

    logger.info(f"Testing pipeline with Bug ID: {bug_id}")
    logger.info(f"Bug Trace: {bug_trace[:100]}..., Raw Text Length: {len(str(bug_trace))} characters")
    logger.info(f"Review: {user_review[:50]}..., User Review Length: {len(str(user_review))} characters")

    
    # Run the pipeline!
    try:
        result = run_pipeline(bug_trace=str(bug_trace), user_review=str(user_review))
        
        print("\n" + "="*50)
        print("🎉 PIPELINE EXECUTION SUCCESSFUL 🎉")
        print("="*50)
        print("\n[ FINAL STRUCTURED OUTPUT ]\n")
        print(result.model_dump_json(indent=2))
        print("\n" + "="*50)
        
    except Exception as e:
        logger.exception(f"Pipeline failed during execution: {e}")

if __name__ == "__main__":
    main()