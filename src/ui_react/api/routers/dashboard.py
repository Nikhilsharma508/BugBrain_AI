from fastapi import APIRouter
import pandas as pd
import json
import yaml
from pathlib import Path

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
JSON_PATH = PROJECT_ROOT / "Data" / "processed" / "processed_bug_reports.json"
POLICIES_DIR = PROJECT_ROOT / "src" / "policies"

def load_policies():
    severities = ["P1_Critical", "P2_High", "P3_Medium", "P4_Low"]
    teams = ["Platform-Team"]
    sev_path = POLICIES_DIR / "severity_policy.yaml"
    team_path = POLICIES_DIR / "team_routing.yaml"
    if sev_path.exists():
        with open(sev_path, "r") as f:
            data = yaml.safe_load(f)
            if "severity_levels" in data:
                severities = [v.get("label", k) for k, v in data["severity_levels"].items()]
    if team_path.exists():
        with open(team_path, "r") as f:
            data = yaml.safe_load(f)
            if "teams" in data:
                teams = list(data["teams"].keys())
    return severities, teams

def load_data():
    if not JSON_PATH.exists(): return pd.DataFrame()
    with open(JSON_PATH, "r") as f: data = json.load(f)
    flat = []
    for k, v in data.items():
        flat.append({
            "Id": int(k),
            "Severity": v.get("severity", "Unknown"),
            "Owner": v.get("suggested_owner", "Unassigned"),
            "Summary": v.get("issue_summary", ""),
            "Error": v.get("technical_details", {}).get("detected_error", "N/A"),
            "Timestamp": v.get("technical_details", {}).get("timestamp", "N/A")
        })
    return pd.DataFrame(flat)

@router.get("/")
def get_dashboard_data():
    df = load_data()
    all_severities, all_teams = load_policies()
    if df.empty: return {"status": "empty"}
    
    top_sev = df["Severity"].mode()[0] if not df["Severity"].empty else "N/A"
    top_owner = df["Owner"].mode()[0] if not df["Owner"].empty else "N/A"
    avg_char = int(df["Summary"].str.len().mean()) if not df["Summary"].empty else 0
    
    sev_counts = df["Severity"].value_counts().reindex(all_severities, fill_value=0).to_dict()
    team_counts = df["Owner"].value_counts().reindex(all_teams, fill_value=0).to_dict()
    
    error_counts = df["Error"].value_counts().head(10).to_dict()
    recent = df[["Id", "Severity", "Owner", "Summary", "Timestamp"]].sort_values("Id", ascending=True).tail(20).to_dict(orient="records")
    
    return {
        "status": "ok",
        "metrics": {
            "total_reports": len(df),
            "top_severity": top_sev,
            "top_owner": top_owner.split('-')[0] if top_owner else "N/A",
            "avg_summary_length": avg_char
        },
        "severity_counts": sev_counts,
        "team_counts": team_counts,
        "error_patterns": error_counts,
        "recent_reports": recent
    }
