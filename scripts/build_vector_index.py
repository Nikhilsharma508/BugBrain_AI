# scripts/build_vector_index.py — Vector Index Builder
#
# PURPOSE:
#   One-shot script to build the FAISS/ChromaDB vector index from
#   historical bug report data. This ensures the app boots with a
#   "warm" index for duplicate detection.
#
# WHAT IT DOES:
#   1. Reads processed bug report data from data/raw/
#   2. Also read the it's output json from data/processed/
#   3. Generates embeddings for each report
#   4. Stores embeddings in FAISS or ChromaDB index
#   5. Saves the index to data/vector_store/
#
# USAGE:
#   python scripts/build_vector_index.py
#
# PREREQUISITES:
#   - Run scripts/load_csv_data.py first
#   - OPENAI_API_KEY must be set in .env
#
# TODO:
#   - Load data from data/raw/
#   - Use EmbeddingManager to generate embeddings
#   - Use VectorStoreManager to build and save the index
#   - Add progress bar for large datasets

import sys
import os
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Add project root to PYTHONPATH so we can import src
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.duplicate_detection.vector_store import get_indexed_ids, add_reports_to_index
from src.telemetry.logger import get_logger

logger = get_logger("build_vector_index")

def main():
    logger.info("Setting up vector index builder...")

    raw_dir = project_root / "Data" / "raw"
    csv_path = raw_dir / "processed_bug_report.csv"
    processed_dir = project_root / "Data" / "processed"

    if not csv_path.exists():
        logger.error(f"Could not find CSV at {csv_path}")
        return

    logger.info(f"Loading data from {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"Failed to read CSV: {e}")
        return

    # Check which IDs are already indexed to avoid recalculation
    indexed_ids = get_indexed_ids()
    logger.info(f"Found {len(indexed_ids)} existing reports in the vector store.")

    texts_to_embed = []
    metadatas = []

    json_path = processed_dir / "processed_bug_reports.json"
    processed_data = {}
    if json_path.exists():
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                processed_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load processed JSON data: {e}")

    for index, row in tqdm(df.iterrows(), total=len(df)):
        bug_id = str(row.get("Id", ""))
        
        # 1. Skip if already indexed by checking the ID directly
        if not bug_id or bug_id in indexed_ids:
            continue
            
        # Skip if JSON doesn't exist (means it wasn't processed yet or load_json_data didn't run)
        if bug_id not in processed_data:
            continue
            
        bug_trace = str(row.get("Bug Details", ""))
        user_review = str(row.get("User Review", "No user review provided"))

        try:
            triage_data = processed_data[bug_id]
                
            # Combine all fields except the raw bug trace (too noisy/long for embeddings)
            combined_text = f"""
            User Review: {user_review}
            Issue Summary: {triage_data.get('issue_summary', '')}
            Steps to Reproduce: {', '.join(triage_data.get('steps_to_reproduce', []))}
            User Impact: {triage_data.get('user_impact_assessment', '')}
            Technical Details: {json.dumps(triage_data.get('technical_details', {}))}
            Triage Reasoning: {triage_data.get('triage_reasoning', '')}
            Severity: {triage_data.get('severity', '')}
            Suggested Owner: {triage_data.get('suggested_owner', '')}
            """
            
            # Use metadata for retrieval context
            metadata = {
                "id": bug_id,
                "issue_summary": triage_data.get('issue_summary', ''),
                "steps": ', '.join(triage_data.get('steps_to_reproduce', [])),
                "user_impact": triage_data.get('user_impact_assessment', ''),
                "technical_details": json.dumps(triage_data.get('technical_details', {})),
                "triage_reasoning": triage_data.get('triage_reasoning', ''),
                "severity": triage_data.get('severity', ''),
                "team": triage_data.get('suggested_owner', '')
            }
            
            texts_to_embed.append(combined_text)
            metadatas.append(metadata)
            
        except Exception as e:
            logger.error(f"Failed to read JSON for Bug ID {bug_id}: {e}")

    if texts_to_embed:
        logger.info(f"Adding {len(texts_to_embed)} new documents to vector store...")
        try:
            add_reports_to_index(texts_to_embed, metadatas)
            logger.info("Successfully added all new documents and saved index.")
        except Exception as e:
            logger.error(f"Failed to save to vector index: {e}")
    else:
        logger.info("No new documents to add to the index.")

if __name__ == "__main__":
    main()
