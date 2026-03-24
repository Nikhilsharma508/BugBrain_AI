import { useState } from 'react';
import {
  Rocket, FileText, Settings, CheckCircle2, RefreshCw, Clock,
  Search, FileSearch, Wrench, User, Code, Brain, Link, Info,
  ChevronUp, ChevronDown
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import GlassCard from '../components/GlassCard';

// ── Helpers ──────────────────────────────────────────────────────────────────

function severityColor(severity = '') {
  if (severity.includes('P1')) return '#ff6b6b';
  if (severity.includes('P2')) return '#ff9800';
  if (severity.includes('P3')) return '#ffc107';
  return '#4caf50';
}

// ── CONFIGURATION (Thresholds for similarity colors) ───────────────────────
const SIMILARITY_THRESHOLDS = {
  HIGH: 90,   // RED Case (>= 90%)
  MEDIUM: 75, // ORANGE Case (>= 75%)
  LOW: 50,    // YELLOW Case (>= 50%)
  NONE: 0     // GREEN Case (Any lower)
};

function similarityColor(pct) {
  if (pct >= SIMILARITY_THRESHOLDS.HIGH) return '#ff6b6b';   // Red
  if (pct >= SIMILARITY_THRESHOLDS.MEDIUM) return '#ff9800'; // Orange
  if (pct >= SIMILARITY_THRESHOLDS.LOW) return '#ffc107';    // Yellow
  return '#4caf50';                                          // Green
}

// ── Sub-components ────────────────────────────────────────────────────────────

function StatusItem({ name, s }) {
  const Icon = s.complete ? CheckCircle2 : s.active ? RefreshCw : Clock;
  const border = s.complete ? '#64d9ff' : s.active ? '#ffc107' : 'rgba(100,150,220,0.3)';
  const bg = s.complete ? 'rgba(50,100,80,0.3)' : s.active ? 'rgba(150,100,20,0.2)' : 'rgba(10,20,35,0.5)';
  const color = s.complete ? '#64d9ff' : s.active ? '#ffc107' : '#b0c4de';

  return (
    <div style={{ background: bg, borderLeft: `4px solid ${border}`, borderRadius: 8, padding: '0.8rem', marginBottom: '0.5rem' }}>
      <p style={{ color, fontWeight: 800, margin: 0, fontSize: '0.95rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Icon size={16} className={s.active ? 'rotate-anim' : ''} /> {name}
      </p>
      <p style={{ color: '#b0c4de', margin: '0.3rem 0 0 0', fontSize: '0.85rem', whiteSpace: 'pre-wrap' }}>{s.desc}</p>
    </div>
  );
}

function SectionDivider() {
  return <hr style={{ border: 'none', borderTop: '1px solid rgba(100,150,220,0.2)', margin: '1rem 0' }} />;
}

function StackFrames({ frames }) {
  const [open, setOpen] = useState(false);
  if (!frames || frames.length === 0) return null;
  return (
    <div style={{ marginTop: '0.75rem' }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{ background: 'rgba(100,182,255,0.1)', border: '1px solid rgba(100,150,220,0.3)', borderRadius: 8, color: 'var(--text-accent)', padding: '0.5rem 1rem', cursor: 'pointer', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}
      >
        {open ? <ChevronUp size={16} /> : <ChevronDown size={16} />} View Key Stack Frames ({frames.length})
      </button>
      {open && (
        <div style={{ marginTop: '0.5rem' }}>
          {frames.map((frame, i) => (
            <div key={i} style={{ marginBottom: '0.5rem' }}>
              <p style={{ color: '#64d9ff', fontWeight: 700, margin: '0.3rem 0', fontSize: '0.85rem' }}>Frame {i + 1}</p>
              <pre style={{ background: 'rgba(10,20,35,0.8)', border: '1px solid rgba(100,150,220,0.2)', borderRadius: 8, color: '#64d9ff', padding: '0.75rem', fontSize: '0.8rem', overflowX: 'auto', margin: 0 }}>{frame}</pre>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function TriageReportFilled({ result }) {
  const sev = result.severity || '';
  const sevColor = severityColor(sev);
  const tech = result.technical_details || {};

  return (
    <div>
      <h3 style={{ color: 'var(--text-accent)', marginTop: 0, textAlign: 'center' }}>FINAL TRIAGE REPORT</h3>

      {/* Severity + Owner */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
        <div style={{ flex: 1, textAlign: 'center', padding: '1rem', background: `rgba(${parseInt(sevColor.slice(1, 3), 16)},${parseInt(sevColor.slice(3, 5), 16)},${parseInt(sevColor.slice(5, 7), 16)},0.15)`, border: `2px solid ${sevColor}`, borderRadius: 20 }}>
          <p style={{ color: sevColor, fontWeight: 900, fontSize: '1.5rem', margin: '0.5rem 0' }}>{sev}</p>
          <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '0.85rem' }}>Assigned Severity</p>
        </div>
        <div style={{ flex: 1, textAlign: 'center', padding: '1rem', background: 'rgba(100,182,255,0.15)', border: '2px solid #64b6ff', borderRadius: 20 }}>
          <p style={{ color: 'var(--text-accent)', fontWeight: 900, fontSize: '1.5rem', margin: '0.5rem 0' }}>{result.suggested_owner}</p>
          <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '0.85rem' }}>Suggested Owner</p>
        </div>
      </div>

      <SectionDivider />

      {/* Issue Summary */}
      <h4 style={{ color: '#64d9ff', fontWeight: 800, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <FileSearch size={20} /> Issue Summary
      </h4>
      <p style={{ color: '#e0e6ff', lineHeight: 1.6 }}>{result.issue_summary}</p>

      <SectionDivider />

      {/* Steps to Reproduce */}
      <h4 style={{ color: '#64d9ff', fontWeight: 800, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Wrench size={20} /> Steps to Reproduce
      </h4>
      {(result.steps_to_reproduce || []).length === 0 ? (
        <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>No reproduction steps extracted.</p>
      ) : (
        <ol style={{ color: '#e0e6ff', paddingLeft: '1.2rem', lineHeight: 1.8 }}>
          {result.steps_to_reproduce.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      )}

      <SectionDivider />

      {/* User Impact */}
      {result.user_impact_assessment && (
        <>
          <h4 style={{ color: '#64d9ff', fontWeight: 800, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <User size={20} /> User Impact
          </h4>
          <p style={{ color: '#e0e6ff', lineHeight: 1.6 }}>{result.user_impact_assessment}</p>
          <SectionDivider />
        </>
      )}

      {/* Technical Details */}
      <h4 style={{ color: '#64d9ff', fontWeight: 800, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Code size={20} /> Technical Details
      </h4>
      <div style={{ background: 'rgba(20,35,60,0.6)', borderLeft: '4px solid #64b6ff', borderRadius: 8, padding: '1rem' }}>
        {tech.detected_error && (
          <p style={{ color: '#b0c4de', margin: '0.4rem 0' }}>
            <strong>Detected Error: </strong><span style={{ color: '#64d9ff' }}>{tech.detected_error}</span>
          </p>
        )}
        {tech.environment && (
          <p style={{ color: '#b0c4de', margin: '0.4rem 0' }}>
            <strong>Environment: </strong><span style={{ color: '#64d9ff' }}>{tech.environment}</span>
          </p>
        )}
        {tech.error_message && (
          <p style={{ color: '#b0c4de', margin: '0.4rem 0' }}>
            <strong>Error Message:</strong><br />
            <code style={{ color: '#e0e6ff', fontFamily: 'monospace', fontSize: '0.9rem' }}>{tech.error_message}</code>
          </p>
        )}
        {tech.timestamp && (
          <p style={{ color: '#b0c4de', margin: '0.4rem 0' }}>
            <strong>Timestamp: </strong><span style={{ color: '#b0c4de' }}>{tech.timestamp}</span>
          </p>
        )}
        <StackFrames frames={tech.key_stack_frames} />
      </div>

      {/* Triage Reasoning */}
      {result.triage_reasoning && (
        <>
          <SectionDivider />
          <h4 style={{ color: '#64d9ff', fontWeight: 800, marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Brain size={20} /> Triage Reasoning
          </h4>
          <div className="markdown-body" style={{ color: '#e0e6ff', lineHeight: 1.6, fontSize: '0.9rem' }}>
            <ReactMarkdown>{result.triage_reasoning}</ReactMarkdown>
          </div>
        </>
      )}
    </div>
  );
}

function TriageReportEmpty() {
  return (
    <div>
      <h3 style={{ color: 'var(--text-accent)', marginTop: 0, textAlign: 'center' }}>FINAL TRIAGE REPORT</h3>
      <p style={{ color: 'var(--text-secondary)', textAlign: 'center' }}>Submit a report to see the analysis</p>
      <div style={{ display: 'flex', gap: '1rem', margin: '1.5rem 0' }}>
        <div style={{ flex: 1, textAlign: 'center', padding: '1.5rem', background: 'rgba(10,20,35,0.4)', border: '2px solid rgba(100,150,220,0.3)', borderRadius: 12 }}>
          <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '0.9rem', fontWeight: 700 }}>Assigned Severity</p>
          <h2 style={{ color: 'rgba(100,150,220,0.5)', margin: '0.5rem 0 0 0' }}>--</h2>
        </div>
        <div style={{ flex: 1, textAlign: 'center', padding: '1.5rem', background: 'rgba(10,20,35,0.4)', border: '2px solid rgba(100,150,220,0.3)', borderRadius: 12 }}>
          <p style={{ color: 'var(--text-secondary)', margin: 0, fontSize: '0.9rem', fontWeight: 700 }}>Suggested Owner</p>
          <h2 style={{ color: 'rgba(100,150,220,0.5)', margin: '0.5rem 0 0 0' }}>--</h2>
        </div>
      </div>
      <hr style={{ borderColor: 'rgba(100,150,220,0.2)' }} />
      <h4 style={{ color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <FileSearch size={18} /> Issue Summary
      </h4>
      <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>Awaiting input...</p>
      <h4 style={{ color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
        <Wrench size={18} /> Steps to Reproduce
      </h4>
      <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic' }}>Awaiting input...</p>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────
import { useTriage } from '../context/TriageContext';

export default function TriagePipeline() {
  const {
    bugTrace, setBugTrace,
    userReview, setUserReview,
    isRunning, setIsRunning,
    error, setError,
    status, setStatus,
    finalResult, setFinalResult,
    similarReports, setSimilarReports,
    combinedText, setCombinedText,
    defaultStatus
  } = useTriage();

  const runPipeline = async () => {
    if (!bugTrace.trim()) return;
    setIsRunning(true);
    setError('');
    setFinalResult(null);
    setSimilarReports([]);
    setStatus({
      preprocess: { active: true, complete: false, desc: 'Processing incoming text...' },
      extract: { active: false, complete: false, desc: 'Waiting for input...' },
      duplicate_detection: { active: false, complete: false, desc: 'Waiting for input...' },
      triage: { active: false, complete: false, desc: 'Waiting for input...' },
    });

    try {
      const res = await fetch('http://localhost:8000/api/triage/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bug_trace: bugTrace, user_review: userReview }),
      });

      if (!res.ok) throw new Error(`Server error: ${res.status}`);

      const reader = res.body.getReader();
      const decoder = new TextDecoder('utf-8');
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // keep incomplete tail

        for (const line of lines) {
          if (!line.trim()) continue;
          let event;
          try { event = JSON.parse(line); } catch { continue; }
          const node = event.node_name;

          if (node === 'preprocess') {
            setStatus(prev => ({
              ...prev,
              preprocess: { active: false, complete: true, desc: '[Logger] Logged regex rules applied.' },
              extract: { active: true, complete: false, desc: 'Calling LLM for extraction...' },
            }));
          } else if (node === 'extract') {
            setStatus(prev => ({
              ...prev,
              extract: { active: false, complete: true, desc: '[LangChain] Extracting structured JSON.\nSummary created.' },
              duplicate_detection: { active: true, complete: false, desc: 'Searching FAISS vector DB...' },
            }));
          } else if (node === 'duplicate_detection') {
            const sim = event.current_state?.similar_reports || [];
            setStatus(prev => ({
              ...prev,
              duplicate_detection: {
                active: false, complete: true,
                desc: `[FAISS] Vector similarity search finished.\nMatched: ${sim.length}`,
              },
              triage: { active: true, complete: false, desc: 'Applying severity policies...' },
            }));
          } else if (node === 'triage') {
            setStatus(prev => ({
              ...prev,
              triage: { active: false, complete: true, desc: '[Policy] Severity rules applied.\nRouting suggested.' },
            }));
          } else if (node === 'completed') {
            const result = event.final_triage_result;
            const reports = event.similar_reports || [];
            const tech = result?.technical_details || {};
            const ct = `User Review: ${userReview}\nIssue Summary: ${result?.issue_summary}\nSteps to Reproduce: ${(result?.steps_to_reproduce || []).join(', ')}\nUser Impact: ${result?.user_impact_assessment}\nTechnical Details: ${JSON.stringify(tech)}`;
            setFinalResult(result);
            setSimilarReports(reports);
            setCombinedText(ct);
          } else if (node === 'error') {
            setError(event.error || 'Unknown pipeline error');
          }
        }
      }
    } catch (e) {
      setError(e.message || 'Error connecting to backend API. Make sure FastAPI is running on port 8000.');
    } finally {
      setIsRunning(false);
    }
  };

  const handleCommit = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/triage/commit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bug_trace: bugTrace, user_review: userReview, triage_result: finalResult, similar_reports: similarReports, combined_text: combinedText }),
      });
      const data = await res.json();
      if (data.status === 'success') {
        alert(`Successfully committed Bug Report #${data.new_id}!`);
        setFinalResult(null);
        setSimilarReports([]);
        setBugTrace('');
        setUserReview('');
        setStatus(defaultStatus);
      } else {
        alert('Commit failed: ' + JSON.stringify(data));
      }
    } catch (e) {
      alert('Error committing: ' + e.message);
    }
  };

  return (
    <div>
      <h1 style={{ color: 'var(--text-accent)', textAlign: 'center', fontSize: '2.5rem', margin: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '15px' }}>
        <Rocket size={40} /> Run Triage Pipeline
      </h1>
      <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginBottom: '2rem' }}>
        Submit a bug report and optional review to trigger the triage agents
      </p>

      {error && (
        <div style={{ background: 'rgba(178,34,34,0.2)', border: '2px solid #ff6b6b', borderRadius: 12, color: '#ff9999', padding: '1rem', marginBottom: '1.5rem' }}>
          ⚠️ {error}
        </div>
      )}

      <div className="grid-3-col">
        {/* ── Left Column ── */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <GlassCard>
            <h3 style={{ color: 'var(--text-accent)', marginTop: 0, display: 'flex', alignItems: 'center', gap: '10px' }}>
              <FileText size={20} /> Submit New Report
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.5rem', display: 'block' }}>Bug Trace / Log Dump *</label>
                <textarea rows={9} placeholder="Paste your raw crash logs or stack traces here..." value={bugTrace} onChange={e => setBugTrace(e.target.value)} />
              </div>
              <div>
                <label style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '0.5rem', display: 'block' }}>User Review (Optional)</label>
                <textarea rows={3} placeholder="User comments or extra context..." value={userReview} onChange={e => setUserReview(e.target.value)} />
              </div>
              <button className="primary" onClick={runPipeline} disabled={isRunning || !bugTrace.trim()} style={{ width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                {isRunning ? <RefreshCw size={18} className="rotate-anim" /> : <Search size={18} />}
                {isRunning ? 'Running Analysis...' : 'Run Analysis'}
              </button>
            </div>
          </GlassCard>

          <GlassCard>
            <h4 style={{ color: '#64d9ff', margin: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Settings size={18} /> Pipeline Live Status
            </h4>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1rem' }}>4 key architecture stages:</p>
            <StatusItem name="Preprocessing" s={status.preprocess} />
            <StatusItem name="Extraction" s={status.extract} />
            <StatusItem name="Duplicate Detection" s={status.duplicate_detection} />
            <StatusItem name="Triage" s={status.triage} />
          </GlassCard>
        </div>

        {/* ── Middle Column ── */}
        <GlassCard style={{ overflowY: 'auto', maxHeight: '90vh' }}>
          {finalResult
            ? <TriageReportFilled result={finalResult} />
            : <TriageReportEmpty />
          }
          {finalResult && (
            <button className="primary" style={{ width: '100%', marginTop: '1.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }} onClick={handleCommit}>
              <CheckCircle2 size={18} /> Ready to Commit
            </button>
          )}
        </GlassCard>

        {/* ── Right Column ── */}
        <GlassCard>
          <h4 style={{ color: '#64d9ff', marginTop: 0, display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Search size={18} /> RAG Similarity Search
          </h4>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginBottom: '1rem' }}>(FAISS/ChromaDB)</p>

          {!finalResult && (
            <p style={{ color: 'var(--text-secondary)', fontStyle: 'italic', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Info size={14} /> Submit a report to search for similar historical issues.
            </p>
          )}

          {finalResult && similarReports.length === 0 && (
            <div style={{ background: 'rgba(70,130,180,0.2)', border: '2px solid #64b6ff', color: '#add8e6', borderRadius: 12, padding: '1rem', fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Info size={18} /> No similar reports found above the similarity threshold.
            </div>
          )}

          {finalResult && similarReports.map((rep, i) => {
            const pct = (rep.similarity_score || 0) * 100;
            const col = similarityColor(pct);
            return (
              <DuplicateCard key={i} rep={rep} pct={pct} col={col} index={i + 1} />
            );
          })}
        </GlassCard>
      </div>
    </div>
  );
}

function DuplicateCard({ rep, pct, col, index }) {
  const [open, setOpen] = useState(index === 1); // auto-open first one
  return (
    <div style={{ background: 'rgba(15,28,50,0.7)', border: '1px solid rgba(100,150,220,0.3)', borderRadius: 8, marginBottom: '1rem', overflow: 'hidden' }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{ width: '100%', background: 'none', border: 'none', cursor: 'pointer', padding: '0.75rem 1rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center', color: 'var(--text-primary)' }}
      >
        <span style={{ fontWeight: 700, fontSize: '0.9rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Link size={16} color={col} /> POTENTIAL DUPLICATE {index} — Match: {pct.toFixed(1)}%
        </span>
        <span style={{ color: 'var(--text-secondary)' }}>{open ? <ChevronUp size={16} /> : <ChevronDown size={16} />}</span>
      </button>
      {open && (
        <div style={{ padding: '0.75rem 1rem', borderTop: '1px solid rgba(100,150,220,0.2)' }}>
          <div style={{
            background: `${col}15`, // Using the hex color with 0.15 opacity
            borderLeft: `4px solid ${col}`,
            borderRadius: 8,
            padding: '0.75rem',
            marginBottom: '0.75rem'
          }}>
            <p style={{ color: col, fontWeight: 900, margin: 0 }}>Similarity: {pct.toFixed(2)}%</p>
          </div>
          <p style={{ color: '#b0c4de', margin: '0.3rem 0', fontSize: '0.9rem' }}>
            <strong>ID: </strong><span style={{ color: 'var(--text-accent)' }}>{rep.id}</span>
          </p>
          <p style={{ color: '#e0e6ff', margin: '0.3rem 0', fontSize: '0.9rem' }}>
            <strong>Summary: </strong>{rep.summary}
          </p>
          {rep.steps && (
            <p style={{ color: '#b0c4de', margin: '0.3rem 0', fontSize: '0.85rem' }}>
              <strong>Steps: </strong>{rep.steps}
            </p>
          )}
          <p style={{ color: '#b0c4de', margin: '0.3rem 0', fontSize: '0.85rem' }}>
            <strong>Severity: </strong><span style={{ color: '#ff9800', fontWeight: 700 }}>{rep.severity}</span>
          </p>
          <p style={{ color: '#b0c4de', margin: '0.3rem 0', fontSize: '0.85rem' }}>
            <strong>Team: </strong><span style={{ color: '#64d9ff' }}>{rep.team}</span>
          </p>
        </div>
      )}
    </div>
  );
}
