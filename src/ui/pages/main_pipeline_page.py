"""
ui/pages/main_pipeline_page.py — Core Triage Pipeline UI
----------------------------------------------------------
PURPOSE:
    Renders the form to accept bug reports and user reviews,
    triggers the orchestrator pipeline, and displays results in a 3-column layout.
"""

import streamlit as st
import time
import json
import pandas as pd
from pathlib import Path
from src.agents.orchestrator import run_pipeline
from src.ui.components import result_display
from src.duplicate_detection.similarity import search_similar_reports
from src.duplicate_detection.vector_store import add_reports_to_index

# Absolute paths for data
project_root = Path(__file__).resolve().parent.parent.parent.parent
raw_dir = project_root / "Data" / "raw"
csv_path = raw_dir / "processed_bug_report.csv"
processed_dir = project_root / "Data" / "processed"

def get_next_id() -> str:
    """Gets the next incremented ID from the CSV."""
    if not csv_path.exists():
        return "1"
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            return "1"
        # Try to find max integer ID
        max_id = 0
        for val in df["Id"].dropna():
            try:
                if int(val) > max_id:
                    max_id = int(val)
            except ValueError:
                pass
        return str(max_id + 1)
    except Exception:
        import uuid
        return str(uuid.uuid4())[:8]

def render():
    st.markdown(
        "<h1 style='text-align: center; color: #64b6ff; margin-bottom: 0; font-weight: 900; font-size: 2.5rem;'>🚀 Run Triage Pipeline</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align: center; color: #b0c4de; margin-bottom: 2rem; font-size: 1rem;'>Submit a bug report and optional review to trigger the triage agents</p>",
        unsafe_allow_html=True
    )

    # We use a 3-column layout
    col_left, col_mid, col_right = st.columns([1.2, 1.2, 1.2], gap="large")

    with col_left:
        # Form inputs
        with st.form("triage_form"):
            st.markdown(
                "<h3 style='color: #64b6ff; font-weight: 900; margin-top: 0;'>📋 Submit New Report</h3>",
                unsafe_allow_html=True
            )
            bug_trace = st.text_area(
                "Bug Trace / Log Dump / Stack Trace",
                height=250,
                placeholder="Paste your raw crash logs or application errors here...",
                help="This is the raw technical output that needs parsing."
            )
            
            user_review = st.text_area(
                "User Review (Optional)",
                height=100,
                placeholder="User comments, steps they tried, or extra context...",
                help="Optional natural language context."
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🔍 Run Analysis", type="primary", use_container_width=True)

    if submitted:
        if not bug_trace.strip():
            st.error("Please provide a Bug Trace to run the analysis.")
            return

        with st.spinner("Agents are analyzing the logs and running triage..."):
            try:
                start_time = time.time()
                
                # 1. Pipeline Extraction
                result = run_pipeline(bug_trace=bug_trace, user_review=user_review)
                duration = time.time() - start_time
                
                # 2. Duplicate Detection
                # Combine info for semantic search matching our index build process (exclude raw trace)
                tech_details_dict = result.technical_details.model_dump() if hasattr(result.technical_details, 'model_dump') else result.technical_details
                combined_text = f"""
                User Review: {user_review}
                Issue Summary: {result.issue_summary}
                Steps to Reproduce: {', '.join(result.steps_to_reproduce)}
                User Impact: {result.user_impact_assessment}
                Technical Details: {json.dumps(tech_details_dict)}
                Triage Reasoning: {result.triage_reasoning}
                Severity: {result.severity}
                Suggested Owner: {result.suggested_owner}
                """
                similar_reports = search_similar_reports(combined_text)
                
                st.session_state["last_result"] = result
                st.session_state["last_bug_trace"] = bug_trace
                st.session_state["last_user_review"] = user_review
                st.session_state["last_duration"] = duration
                st.session_state["last_similar"] = similar_reports
                st.session_state["last_combined_text"] = combined_text
                
            except Exception as e:
                st.error(f"Pipeline execution failed: {str(e)}")
                st.exception(e)
                return

    # Render results if we have them in session state
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        duration = st.session_state["last_duration"]
        similar_reports = st.session_state["last_similar"]

        # Left Column: Pipeline Live Status (Simulated Logs for UI flavor)
        with col_left:
            with st.container(border=True):
                st.markdown(
                    "<h4 style='color: #64d9ff; font-weight: 900; margin-top: 0;'>⚙️ Pipeline Live Status</h4>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<p style='color: #b0c4de; font-size: 0.9rem; margin-bottom: 1rem;'>5 key architecture stages:</p>",
                    unsafe_allow_html=True
                )
                
                # Status items with better styling
                status_items = [
                    ("Preprocessing", "✅ [Filter] Stripped emotion, memory dumps.\n[Logger] Logged regex rules applied."),
                    ("Extraction", "✅ [LangChain] Extracting structured JSON.\nSummary created."),
                    ("Duplicate Detection", f"✅ [FAISS] Vector similarity search initiated.\nThreshold: 85%. Matched: {len(similar_reports)}"),
                    ("Triage", "✅ [Policy] Severity rules applied.\nRouting suggested."),
                    ("Output", "✅ Structure standardized for export."),
                ]
                
                for stage, description in status_items:
                    st.markdown(
                        f"""
                        <div style='background: rgba(50, 100, 80, 0.3); border-left: 4px solid #64d9ff; border-radius: 8px; padding: 0.8rem; margin-bottom: 0.5rem;'>
                            <p style='color: #64d9ff; font-weight: 800; margin: 0; font-size: 0.95rem;'>✅ {stage}</p>
                            <p style='color: #b0c4de; margin: 0.3rem 0 0 0; font-size: 0.85rem; white-space: pre-wrap;'>{description}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Middle Column: Final Triage Report
        with col_mid:
            with st.container(border=True):
                result_display.render_triage_result(result, duration)
                
                st.markdown("<hr style='border: 1px solid rgba(100, 150, 220, 0.2);'>", unsafe_allow_html=True)
                
                # Ready to Commit Button
                if st.button("✅ Ready to Commit", type="primary", use_container_width=True, key="commit_btn"):
                    with st.spinner("Committing to standard dataset & vector store..."):
                        try:
                            new_id = get_next_id()
                            bug_trace = st.session_state["last_bug_trace"]
                            user_review = st.session_state["last_user_review"]
                            
                            # 1. Update CSV
                            new_row = pd.DataFrame([{"Id": new_id, "Bug Details": bug_trace, "User Review": user_review}])
                            if csv_path.exists():
                                df = pd.read_csv(csv_path)
                                df = pd.concat([df, new_row], ignore_index=True)
                            else:
                                os.makedirs(raw_dir, exist_ok=True)
                                df = new_row
                            df.to_csv(csv_path, index=False)
                            
                            # 2. Save JSON
                            os.makedirs(processed_dir, exist_ok=True)
                            json_path = processed_dir / "processed_bug_reports.json"
                            
                            processed_data = {}
                            if json_path.exists():
                                with open(json_path, "r", encoding="utf-8") as f:
                                    processed_data = json.load(f)
                                    
                            processed_data[new_id] = json.loads(result.model_dump_json())
                            
                            with open(json_path, "w", encoding="utf-8") as f:
                                json.dump(processed_data, f, indent=2)
                                
                            # 3. Add to FAISS Vector Store
                            combined_text = st.session_state["last_combined_text"]
                            metadata = {
                                "id": new_id,
                                "issue_summary": result.issue_summary,
                                "steps": ', '.join(result.steps_to_reproduce),
                                "severity": result.severity,
                                "team": result.suggested_owner
                            }
                            
                            add_reports_to_index([combined_text], [metadata])
                            
                            st.success(f"Successfully committed Bug Report #{new_id}!")
                            # Clear session state so it doesn't try to commit again
                            del st.session_state["last_result"]
                            
                        except Exception as e:
                            st.error(f"Commit failed: {e}")

        # Right Column: RAG Similarity Search
        with col_right:
            with st.container(border=True):
                st.markdown(
                    "<h4 style='color: #64d9ff; font-weight: 900; margin-top: 0;'>🔍 RAG Similarity Search</h4>",
                    unsafe_allow_html=True
                )
                st.markdown(
                    "<p style='color: #b0c4de; font-size: 0.85rem;'>(FAISS/ChromaDB)</p>",
                    unsafe_allow_html=True
                )
                
                if not similar_reports:
                    st.info("ℹ️ No similar reports found above the threshold.")
                else:
                    for i, rep in enumerate(similar_reports):
                        score_pct = rep.get('similarity_score', 0) * 100
                        
                        # Similarity score with color gradient
                        if score_pct >= 90:
                            score_color = "#ff6b6b"  # High similarity - red
                        elif score_pct >= 75:
                            score_color = "#ff9800"  # Medium - orange
                        else:
                            score_color = "#ffc107"  # Lower - yellow
                        
                        with st.expander(
                            f"🔗 POTENTIAL DUPLICATE {i+1} — Match: {score_pct:.1f}%",
                            expanded=(i == 0)
                        ):
                            st.markdown(
                                f"<div style='background: rgba(100, 182, 255, 0.15); border-left: 4px solid {score_color}; border-radius: 8px; padding: 1rem;'>"
                                f"<p style='color: {score_color}; font-weight: 900; margin: 0;'>Similarity: {score_pct:.2f}%</p>"
                                f"</div>",
                                unsafe_allow_html=True
                            )
                            
                            st.markdown(
                                f"<p style='color: #b0c4de; font-size: 0.9rem; margin-top: 0.5rem;'><strong>ID:</strong> <span style='color: #64b6ff;'>{rep.get('id')}</span></p>"
                                f"<p style='color: #e0e6ff; margin: 0.3rem 0;'><strong>Summary:</strong> {rep.get('summary')}</p>"
                                f"<p style='color: #b0c4de; margin: 0.3rem 0;'><strong>Steps:</strong> {rep.get('steps')}</p>"
                                f"<p style='color: #b0c4de; margin: 0.3rem 0;'><strong>Severity:</strong> <span style='color: #ff9800; font-weight: 700;'>{rep.get('severity')}</span></p>"
                                f"<p style='color: #b0c4de; margin: 0.3rem 0;'><strong>Team:</strong> <span style='color: #64d9ff;'>{rep.get('team')}</span></p>",
                                unsafe_allow_html=True
                            )
