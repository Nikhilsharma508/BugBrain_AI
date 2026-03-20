import json
import os
import pandas as pd
import yaml
from typing import Dict, List
from src.agents.agent import LLMManager
from src.prompts.evaluation_prompts import JUDGE_SYSTEM_PROMPT, JUDGE_USER_PROMPT

from pydantic import BaseModel, Field

# Paths
JSON_PATH = "Data/processed/processed_bug_reports.json"
CSV_PATH = "Data/raw/processed_bug_report.csv"
SEVERITY_POLICY = "src/policies/severity_policy.yaml"
TEAM_ROUTING = "src/policies/team_routing.yaml"
EVAL_RESULTS_PATH = "Data/processed/evaluation_results.json"

class EvaluationResult(BaseModel):
    fidelity_score: int = Field(..., ge=0, le=10)
    compliance_score: int = Field(..., ge=0, le=10)
    noise_reduction_score: int = Field(..., ge=0, le=10)
    reasoning: str

def load_data():
    with open(JSON_PATH, "r") as f:
        ai_data = json.load(f)
    
    csv_df = pd.read_csv(CSV_PATH)
    
    with open(SEVERITY_POLICY, "r") as f:
        sev_policy = f.read()
    
    with open(TEAM_ROUTING, "r") as f:
        route_policy = f.read()
        
    return ai_data, csv_df, sev_policy, route_policy

def run_evaluation():
    ai_data, csv_df, sev_policy, route_policy = load_data()
    
    # Load default model from .env
    manager = LLMManager() 
    # Bind the evaluation schema for structured output
    judge_llm = manager.get_client_with_structured_output(EvaluationResult)
    
    results = {}
    print(f"🚀 Starting evaluation of {len(ai_data)} reports...")
    
    for bug_id, ai_output in ai_data.items():
        # Find corresponding CSV row
        row = csv_df[csv_df['Id'] == int(bug_id)].iloc[0]
        
        user_prompt = JUDGE_USER_PROMPT.format(
            bug_details=row['Bug Details'],
            user_review=row['User Review'],
            ai_output=json.dumps(ai_output, indent=2),
            severity_policy=sev_policy,
            team_routing=route_policy
        )
        
        print(f"🧐 Judging Report ID: {bug_id}...")
        
        # Using langsmith/langchain invoke pattern
        eval_result = judge_llm.invoke([
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ])
        
        results[bug_id] = eval_result.dict()
        
    # Save results
    with open(EVAL_RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
        
    # Calculate Averages
    f_scores = [r['fidelity_score'] for r in results.values()]
    c_scores = [r['compliance_score'] for r in results.values()]
    n_scores = [r['noise_reduction_score'] for r in results.values()]
    
    print("\n" + "="*40)
    print("📈 EVALUATION COMPLETE")
    print("="*40)
    print(f"Average Extraction Fidelity: {sum(f_scores)/len(f_scores):.2f}/10")
    print(f"Average Policy Compliance:   {sum(c_scores)/len(c_scores):.2f}/10")
    print(f"Average Noise Reduction:     {sum(n_scores)/len(n_scores):.2f}/10")
    print("="*40)
    print(f"Detailed logs saved to: {EVAL_RESULTS_PATH}")

if __name__ == "__main__":
    run_evaluation()
