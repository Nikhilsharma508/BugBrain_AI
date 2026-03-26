import os
import sys
from dotenv import load_dotenv

# Set up paths so we can import src
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.duplicate_detection.similarity import search_similar_reports

def run_test():
    load_dotenv()
    
    query = """
    User Review: The application crashes instantly when I try to log in using Google OAuth. It worked fine yesterday.
    Issue Summary: App crash on login
    Steps to Reproduce: 1. Launch App, 2. Tap Google Login
    User Impact: Cannot log in
    Technical Details: {}
    """
    
    strategies = ["cosine", "mmr", "multiquery", "contextual"]
    
    for strategy in strategies:
        print(f"\n--- Testing Strategy: {strategy} ---")
        os.environ["RETRIEVAL_STRATEGY"] = strategy
        try:
            results = search_similar_reports(query, top_k=2, threshold=0.0) # threshold 0.0 to see what we get
            print(f"Found {len(results)} results.")
            for i, r in enumerate(results):
                print(f"  {i+1}: ID={r['id']}, Score={r['similarity_score']:.4f}, Summary={r.get('summary', '')}")
        except Exception as e:
            print(f"FAILED: {e}")

if __name__ == "__main__":
    run_test()
