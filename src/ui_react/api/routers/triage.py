from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time
import json
import os
import pandas as pd
from pathlib import Path

from src.agents.orchestrator import run_pipeline
from src.duplicate_detection.similarity import EMBEDDING_SIMILARITY_THRESHOLD
from src.duplicate_detection.vector_store import add_reports_to_index

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
raw_dir = PROJECT_ROOT / "Data" / "raw"
csv_path = raw_dir / "processed_bug_report.csv"
processed_dir = PROJECT_ROOT / "Data" / "processed"

class TriageRequest(BaseModel):
    bug_trace: str
    user_review: str = ""

def get_next_id() -> str:
    if not csv_path.exists(): return "1"
    try:
        df = pd.read_csv(csv_path)
        if df.empty: return "1"
        return str(int(df["Id"].dropna().astype(float).max()) + 1)
    except:
        import uuid
        return str(uuid.uuid4())[:8]

def serialize_event(event):
    def custom_dump(obj):
        if hasattr(obj, "model_dump"): return obj.model_dump()
        return str(obj)
    return json.dumps(event, default=custom_dump) + "\n"

@router.post("/run")
def run_triage_stream(req: TriageRequest):
    def event_generator():
        try:
            for event in run_pipeline(bug_trace=req.bug_trace, user_review=req.user_review):
                yield serialize_event(event)
        except Exception as e:
            yield serialize_event({"node_name": "error", "error": str(e)})
    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

class CommitRequest(BaseModel):
    bug_trace: str
    user_review: str
    triage_result: dict
    similar_reports: list
    combined_text: str

@router.post("/commit")
def commit_triage(req: CommitRequest):
    try:
        new_id = get_next_id()
        os.makedirs(raw_dir, exist_ok=True)
        if csv_path.exists():
            df = pd.read_csv(csv_path)
        else:
            df = pd.DataFrame(columns=["Id", "Bug Details", "User Review"])
        
        new_row = pd.DataFrame([{
            "Id": int(new_id),
            "Bug Details": req.bug_trace,
            "User Review": req.user_review or "No user review provided"
        }])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_path, index=False)
        
        os.makedirs(processed_dir, exist_ok=True)
        json_path = processed_dir / "processed_bug_reports.json"
        processed_data = {}
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                processed_data = json.load(f)
        processed_data[new_id] = req.triage_result
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(processed_data, f, indent=2)
            
        metadata = {
            "id": new_id,
            "issue_summary": req.triage_result.get("issue_summary", ""),
            "steps": ", ".join(req.triage_result.get("steps_to_reproduce", [])),
            "severity": req.triage_result.get("severity", ""),
            "team": req.triage_result.get("suggested_owner", ""),
        }
        add_reports_to_index([req.combined_text], [metadata])
        
        return {"status": "success", "new_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
