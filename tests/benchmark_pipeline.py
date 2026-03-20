import time
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.agents.orchestrator import run_pipeline

load_dotenv()

SAMPLE_INPUTS = [
    {
        "bug_trace": "java.lang.NullPointerException at com.example.App.onStart(App.java:42)",
        "user_review": "The app crashed as soon as I opened it on my Android phone."
    },
    {
        "bug_trace": "HTTP 500: Internal Server Error at /api/v1/purchase",
        "user_review": "I tried to buy a subscription and it failed with a server error."
    },
    {
        "bug_trace": "Timeout waiting for element #login-button on iPad Safari",
        "user_review": "I can't log in on my iPad. The button never appears."
    },
    {
        "bug_trace": "403 Forbidden: User not authorized to access resource /admin/settings",
        "user_review": "I am an admin but I can't access the settings page."
    },
    {
        "bug_trace": "Out of memory error in background worker process",
        "user_review": "The system seems slow and then some tasks just stop working."
    }
]

def run_benchmarks():
    print(f"{'Input #':<10} | {'Latency (s)':<12} | {'Tokens':<10} | {'Cost ($)':<10}")
    print("-" * 50)
    
    total_latency = 0
    total_tokens = 0
    total_cost = 0
    
    for i, input_data in enumerate(SAMPLE_INPUTS):
        start_time = time.time()
        
        # Capture tokens using OpenAI callback (works for Azure too)
        with get_openai_callback() as cb:
            final_result = None
            for update in run_pipeline(input_data["bug_trace"], input_data["user_review"]):
                if update.get("node_name") == "completed":
                    final_result = update.get("final_triage_result")
            
            latency = time.time() - start_time
            total_latency += latency
            total_tokens += cb.total_tokens
            total_cost += cb.total_cost
            
            print(f"{i+1:<10} | {latency:<12.2f} | {cb.total_tokens:<10} | {cb.total_cost:<10.6f}")

    avg_latency = total_latency / len(SAMPLE_INPUTS)
    print("-" * 50)
    print(f"Average Latency: {avg_latency:.2f}s")
    print(f"Total Tokens: {total_tokens}")
    print(f"Total Estimated Cost: ${total_cost:.6f}")

if __name__ == "__main__":
    run_benchmarks()
