import sys
import os
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Add project root to PYTHONPATH so we can import src
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.agents.orchestrator import run_pipeline
from src.telemetry.logger import get_logger

logger = get_logger("load_json_data")


def main():
    logger.info("Setting up data loader...")

    raw_dir = project_root / "Data" / "raw"
    csv_path = raw_dir / "processed_bug_report.csv"
    processed_dir = project_root / "Data" / "processed"

    if not csv_path.exists():
        logger.error(f"Could not find CSV at {csv_path}")
        return

    os.makedirs(processed_dir, exist_ok=True)

    logger.info(f"Loading data from {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return

    if df.empty:
        logger.error("CSV is empty!")
        return

    logger.info(f"Found {len(df)} reports in CSV. Checking for missing JSONs...")

    processed_count = 0

    json_path = processed_dir / "processed_bug_reports.json"

    processed_data = {}
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                processed_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load existing processed JSON data: {e}")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        bug_id = str(row.get("Id", ""))
        if not bug_id:
            continue

        # Check if already processed
        if bug_id in processed_data:
            continue

        bug_trace = str(row.get("Bug Details", ""))
        user_review = str(row.get("User Review", "No user review provided"))

        try:
            # Run the extraction and triage pipeline
            logger.info(f"Running pipeline for Bug ID: {bug_id}")
            result = run_pipeline(bug_trace=bug_trace, user_review=user_review)

            # Save the JSON representation
            processed_data[bug_id] = json.loads(result.model_dump_json())

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(processed_data, f, indent=2)

            processed_count += 1
            logger.info(f"Processed and saved JSON for Bug ID: {bug_id}")

        except Exception as e:
            logger.error(f"Pipeline failed for Bug ID {bug_id}: {e}")

    logger.info(f"Data loading complete. Generated {processed_count} new JSONs.")


if __name__ == "__main__":
    main()
