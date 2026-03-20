"""
tests/test_pipeline_backend.py — Functional Pipeline Test
-----------------------------------------------------------
PURPOSE:
    Provides a standalone test case to verify the LangGraph-based
    orchestrator and the full bug triage pipeline.

USAGE:
    1. As a script: python tests/test_pipeline_backend.py
    2. As a test: pytest tests/test_pipeline_backend.py -s
"""

import sys
from pathlib import Path
import json
from dotenv import load_dotenv

# Load environment variables (simulate .env loading if not already in environment)
load_dotenv()

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.agents.orchestrator import run_pipeline

SAMPLE_BUG_TRACE = """
Date: Fri May 10 11:46:52 GMT+03:00 2002
java.lang.ClassCastException: org.eclipse.jdt.internal.compiler.ast.FieldDeclaration
	at org.eclipse.jdt.internal.compiler.parser.Parser.buildInitialRecoveryState(Parser.java:539)
	at org.eclipse.jdt.internal.compiler.parser.Parser.parse(Parser.java:500)
	at org.eclipse.jdt.internal.compiler.ast.Initializer.parseStatements(Initializer.java:52)
	at org.eclipse.jdt.internal.compiler.ast.TypeDeclaration.parseMethod(TypeDeclaration.java:695)
	at org.eclipse.jdt.internal.compiler.Compiler.getMethodBodies(Compiler.java:256)
	at org.eclipse.jdt.internal.core.builder.impl.IncrementalImageBuilder.applySourceDelta(IncrementalImageBuilder.java:264)
	at org.eclipse.jdt.internal.core.builder.impl.JavaBuilder.build(JavaBuilder.java:54)
"""

SAMPLE_USER_REVIEW = (
    "I was saving a Java file in Eclipse when the build failed with this error."
)


def test_full_pipeline_execution(bug_trace=SAMPLE_BUG_TRACE, user_review=SAMPLE_USER_REVIEW):
    """Run the orchestrator with one instance and print the JSON result."""
    print("\n" + "=" * 50)
    print("🚀 STARTING BACKEND PIPELINE TEST")
    if bug_trace == SAMPLE_BUG_TRACE:
        print("📝 Using: SAMPLE_BUG_TRACE")
    else:
        print("📝 Using: Validation Input Data")
    print("=" * 50 + "\n")

    final_result = None

    # Run the pipeline generator
    for update in run_pipeline(bug_trace, user_review):
        node_name = update.get("node_name")

        if node_name == "completed":
            final_result = update.get("final_triage_result")
            print("\n✅ PIPELINE CAN RUN SUCCESSFULLY")
        else:
            print(f"🔄 Executing: [{node_name}]...")

    if final_result:
        print("\n" + "=" * 50)
        print("📋 FINAL TRIAGE RESULT (JSON)")
        print("=" * 50)

        # Convert Pydantic model to dict and then formatted JSON
        result_dict = final_result.model_dump()
        print(json.dumps(result_dict, indent=2))
        print("=" * 50 + "\n")

        return result_dict
    else:
        print("\n❌ Pipeline failed to produce a final result.")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run backend pipeline test")
    parser.add_argument(
        "--validation",
        action="store_true",
        help="Use data from 'Validation Data/Validation Input.md'",
    )
    args = parser.parse_args()

    trace = SAMPLE_BUG_TRACE
    review = SAMPLE_USER_REVIEW

    if args.validation:
        val_path = PROJECT_ROOT / "Validation Data" / "Validation Input.md"
        if val_path.exists():
            print(f"📖 Loading validation data from {val_path}...")
            trace = val_path.read_text()
            review = "User is reporting a system crash/lookup error detailed in the attached log."
        else:
            print(f"⚠️ Warning: {val_path} not found. Falling back to sample data.")

    # If run directly as a script, execute the test function
    test_full_pipeline_execution(bug_trace=trace, user_review=review)
