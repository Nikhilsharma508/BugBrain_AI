import { useState, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { motion } from 'framer-motion';
import { useTriage } from '../context/TriageContext';
import {
  Play, FileText, Info,
  Terminal, Database, ListChecks, Bug,
  MessageSquare, Cpu, AlertTriangle
} from 'lucide-react';

// ── Helpers ──────────────────────────────────────────────────────────────────

// ── TYPEWRITER COMPONENT ───────────────────────────────────────────────────
// This component handles the "streaming" reveal animation for text.
// If you want to change the speed or the reveal logic, edit this function.
function Typewriter({ text, speed = 5 }) {
  const [displayed, setDisplayed] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    setDisplayed(''); // Reset when text changes
    setIndex(0);
  }, [text]);

  useEffect(() => {
    if (index < text.length) {
      const timeout = setTimeout(() => {
        setDisplayed(prev => prev + text[index]);
        setIndex(prev => prev + 1);
      }, speed);
      return () => clearTimeout(timeout);
    }
  }, [index, text, speed]);

  return <span>{displayed}</span>;
}

// Helper for markdown streaming
function StreamingMarkdown({ content, speed = 2 }) {
  const [displayed, setDisplayed] = useState('');
  const [index, setIndex] = useState(0);

  useEffect(() => {
    setDisplayed('');
    setIndex(0);
  }, [content]);

  useEffect(() => {
    if (index < (content || '').length) {
      const timeout = setTimeout(() => {
        setDisplayed(prev => prev + content[index]);
        setIndex(prev => prev + 1);
      }, speed);
      return () => clearTimeout(timeout);
    }
  }, [index, content, speed]);

  return <ReactMarkdown>{displayed}</ReactMarkdown>;
}

function getSeverityColor(sev = '') {
  if (sev.includes('P1')) return 'var(--error-red)';
  if (sev.includes('P2')) return 'var(--accent-primary)';
  if (sev.includes('P3')) return 'var(--sev-amber-text)';
  return 'var(--success-green)';
}

function getSimilarityColor(pct) {
  if (pct >= 60) return 'var(--accent-primary)';
  if (pct >= 30) return 'var(--team-blue-text)';
  return 'var(--text-muted)';
}

// ── Sub-components ────────────────────────────────────────────────────────────

function StatusItem({ name, s }) {
  // s.complete => green check
  // s.active => pulsing copper
  // !s.active && !s.complete => gray

  return (
    <div style={{ padding: '12px 0', borderBottom: '1px solid #E8E0D4', display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
      <div style={{ marginTop: '2px', position: 'relative' }}>
        {s.complete ? (
          <div style={{ width: 16, height: 16, borderRadius: '50%', backgroundColor: 'var(--success-green)', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '10px' }}>✓</div>
        ) : s.active ? (
          <>
            <div style={{ width: 16, height: 16, borderRadius: '50%', backgroundColor: 'var(--accent-primary)', position: 'relative', zIndex: 2 }} />
            <div className="status-pulsing" style={{ position: 'absolute', top: 0, left: 0, width: 16, height: 16, borderRadius: '50%', zIndex: 1, backgroundColor: 'rgba(196,122,58,0.25)' }} />
          </>
        ) : (
          <div style={{ width: 16, height: 16, borderRadius: '50%', backgroundColor: 'var(--border)' }} />
        )}
      </div>
      <div>
        <p style={{ margin: 0, fontWeight: 500, fontSize: '13px', color: 'var(--text-primary)', fontFamily: 'Inter, sans-serif' }}>{name}</p>
        <p style={{ margin: '4px 0 0', fontFamily: 'JetBrains Mono, monospace', fontSize: '11px', color: 'var(--text-secondary)', whiteSpace: 'pre-wrap' }}>{s.desc}</p>
      </div>
    </div>
  );
}

function ReportSectionHeader({ title, icon: Icon }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', marginTop: '20px' }}>
      <div className="brand-dot" />
      {Icon && <Icon size={14} color="var(--accent-primary)" style={{ marginLeft: '4px' }} />}
      <span className="section-label">{title}</span>
    </div>
  );
}

function Pill({ text, styleObj }) {
  return (
    <span style={{
      fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '11px',
      letterSpacing: '0.06em', textTransform: 'uppercase',
      padding: '2px 8px', borderRadius: '4px', ...styleObj
    }}>
      {text}
    </span>
  );
}

function TechRow({ label, value }) {
  return (
    <div style={{ display: 'flex', marginBottom: '4px' }}>
      <span style={{ color: 'var(--text-muted)', width: '120px', flexShrink: 0 }}>{label}:</span>
      <span style={{ color: 'var(--text-primary)', fontWeight: 500 }}>{value}</span>
    </div>
  );
}

function TriageReportFilled({ result }) {
  const tech = result.technical_details || {};
  const frames = tech.key_stack_frames || [];

  return (
    <div>
      {/* Header bar */}
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        borderBottom: '1px solid var(--border)', paddingBottom: '12px', marginBottom: '20px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div className="brand-dot" />
            <span className="section-label">Triage Result</span>
          </div>
          <span style={{ fontFamily: 'JetBrains Mono, monospace', color: 'var(--text-muted)', fontSize: '12px' }}>TRG-UNASSIGNED</span>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <Pill text={result.severity || 'P?'} styleObj={{ backgroundColor: 'var(--sev-amber-bg)', color: 'var(--sev-amber-text)', border: '1px solid var(--sev-amber-border)' }} />
          <Pill text={result.suggested_owner || 'TEAM?'} styleObj={{ backgroundColor: 'var(--team-blue-bg)', color: 'var(--team-blue-text)', border: '1px solid var(--team-blue-border)' }} />
        </div>
      </div>

      {/* Issue Summary */}
      <ReportSectionHeader title="Issue Summary" icon={FileText} />
      <p className="body-copy" style={{ color: 'var(--text-primary)' }}>
        <Typewriter text={result.issue_summary || ''} speed={5} />
      </p>

      {/* User Impact Assessment */}
      {result.user_impact_assessment && (
        <>
          <ReportSectionHeader title="User Impact Assessment" icon={AlertTriangle} />
          <p className="body-copy" style={{ color: 'var(--text-primary)' }}>
            <Typewriter text={result.user_impact_assessment || ''} speed={5} />
          </p>
        </>
      )}

      {/* Steps to Reproduce */}
      <ReportSectionHeader title="Steps to Reproduce" icon={ListChecks} />
      {(result.steps_to_reproduce || []).length === 0 ? (
        <p className="body-copy" style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>No steps extracted.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {result.steps_to_reproduce.map((step, i) => (
            <div key={i} style={{ display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
              <div style={{
                width: '18px', height: '18px', borderRadius: '4px', backgroundColor: '#EDE7DC',
                display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
                fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '11px', color: 'var(--text-secondary)'
              }}>
                {i + 1}
              </div>
              <p className="body-copy" style={{ margin: 0, marginTop: '-1px' }}>{step}</p>
            </div>
          ))}
        </div>
      )}

      {/* Technical Details */}
      <ReportSectionHeader title="Technical Details" icon={Terminal} />
      <div style={{
        backgroundColor: 'var(--surface-alt)', border: '1px solid #D5CCBF',
        borderRadius: '8px', padding: '16px', fontFamily: 'JetBrains Mono, monospace', fontSize: '12px'
      }}>
        {tech.detected_error && <TechRow label="Detected Error" value={tech.detected_error} />}
        {tech.component && <TechRow label="Component" value={tech.component} />}
        {tech.file_context && <TechRow label="File Context" value={tech.file_context} />}

        {frames.length > 0 && (
          <div style={{ marginTop: '12px' }}>
            <p style={{ color: 'var(--text-muted)', fontSize: '12px', margin: '0 0 4px', fontFamily: 'JetBrains Mono, monospace' }}>Key Stack Frames ({frames.length}):</p>
            {frames.map((frame, i) => (
              <pre key={i} style={{
                background: 'none', border: 'none', padding: 0, color: 'var(--text-secondary)',
                fontFamily: 'JetBrains Mono, monospace', fontSize: '11px', whiteSpace: 'pre-wrap', marginBottom: '8px'
              }}>
                {frame}
              </pre>
            ))}
          </div>
        )}
      </div>

      {/* Triage Reasoning */}
      {result.triage_reasoning && (
        <>
          <ReportSectionHeader title="Triage Reasoning" icon={Info} />
          <div className="markdown-body" style={{
            backgroundColor: 'var(--surface)', borderLeft: '2px solid var(--accent-primary)',
            borderRadius: '0 6px 6px 0', padding: '12px 16px',
            fontFamily: 'Inter, sans-serif', fontSize: '13px', lineHeight: 1.7, color: 'var(--text-secondary)'
          }}>
            <StreamingMarkdown content={result.triage_reasoning} speed={2} />
          </div>
        </>
      )}
    </div>
  );
}

function TriageAIReveal() {
  const words = ['AI', 'Bug', 'Triage.'];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '24px' }}>
      {/* Animated brand mark */}
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '6px' }}>
        {words.map((word, wi) => (
          <motion.span
            key={wi}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: wi * 0.25, duration: 0.5, ease: 'easeOut' }}
            style={{
              fontFamily: 'Georgia, serif',
              fontSize: wi === 0 ? '36px' : '28px',
              color: wi === 0 ? 'var(--accent-primary)' : 'var(--text-primary)',
              letterSpacing: '-0.02em'
            }}
          >
            {word}
          </motion.span>
        ))}
      </div>

      {/* Streaming hint text */}
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.1, duration: 0.6 }}
        className="body-copy"
        style={{ color: 'var(--text-muted)', fontStyle: 'italic', textAlign: 'center', maxWidth: '240px' }}
      >
        Paste a bug trace to start analysis.
      </motion.p>
    </div>
  );
}

function TriageReportEmpty() {
  return (
    <div style={{
      display: 'flex', height: '100%', alignItems: 'center', justifyContent: 'center'
    }}>
      <TriageAIReveal />
    </div>
  );
}

function DuplicateCard({ rep, pct, index }) {
  const col = getSimilarityColor(pct);
  const [w, setW] = useState('0%');

  useEffect(() => {
    // Animate after mount
    const timer = setTimeout(() => {
      setW(`${pct}%`);
    }, 100 + (index * 100)); // staggered
    return () => clearTimeout(timer);
  }, [pct, index]);

  return (
    <div style={{
      backgroundColor: 'var(--surface)', border: '1px solid var(--border)',
      borderRadius: '8px', padding: '12px', marginBottom: '10px'
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
        <span style={{ fontFamily: 'Inter, sans-serif', fontWeight: 500, fontSize: '12px', color: 'var(--text-primary)' }}>
          Potential Duplicate {index}
        </span>
        <span style={{ fontFamily: 'JetBrains Mono, monospace', fontSize: '12px', color: col }}>
          {pct.toFixed(0)}%
        </span>
      </div>

      {/* Progress bar */}
      <div style={{ height: '4px', borderRadius: '2px', backgroundColor: '#E8E0D4', marginBottom: '10px', overflow: 'hidden' }}>
        <div style={{
          height: '100%', backgroundColor: col, width: w,
          transition: 'width 600ms ease-out'
        }} />
      </div>

      <p style={{
        fontFamily: 'Inter, sans-serif', fontSize: '12px', color: 'var(--text-secondary)',
        margin: '0 0 10px 0', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden'
      }}>
        {rep.summary}
      </p>

      <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
        <span style={{
          fontFamily: 'JetBrains Mono, monospace', fontWeight: 500, fontSize: '10px',
          backgroundColor: 'var(--surface-alt)', color: 'var(--text-muted)',
          border: '1px solid var(--border)', padding: '2px 6px', borderRadius: '4px'
        }}>
          TRG - {rep.id || 'N/A'}
        </span>
        <span style={{
          fontFamily: 'Inter, sans-serif', fontWeight: 500, fontSize: '10px',
          backgroundColor: 'var(--sev-amber-bg)', color: 'var(--sev-amber-text)',
          border: '1px solid var(--sev-amber-border)', padding: '2px 6px', borderRadius: '4px', textTransform: 'uppercase'
        }}>
          {rep.severity || 'N/A'}
        </span>
        <span style={{
          fontFamily: 'Inter, sans-serif', fontWeight: 500, fontSize: '10px',
          backgroundColor: 'var(--team-blue-bg)', color: 'var(--team-blue-text)',
          border: '1px solid var(--team-blue-border)', padding: '2px 6px', borderRadius: '4px', textTransform: 'uppercase'
        }}>
          {rep.team || 'Unassigned'}
        </span>
      </div>

      {rep.steps && (
        <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #E8E0D4' }}>
          <p style={{
            fontFamily: 'Inter, sans-serif', fontSize: '11px', fontWeight: 600,
            color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em', margin: '0 0 4px 0'
          }}>
            Steps to Reproduce
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {(rep.steps.split(', ') || []).map((step, k) => (
              <div key={k} style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
                <div style={{
                  width: '16px', height: '16px', borderRadius: '4px', backgroundColor: '#EDE7DC',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0,
                  fontFamily: 'Inter, sans-serif', fontWeight: 600, fontSize: '10px', color: 'var(--text-secondary)'
                }}>
                  {k + 1}
                </div>
                <p style={{
                  fontFamily: 'Inter, sans-serif', fontSize: '11px', color: 'var(--text-secondary)',
                  margin: 0, marginTop: '-2px', lineHeight: 1.4
                }}>
                  {step}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

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

  // ── RAG Sidebar default width ─────────────────────────────────────────────
  // Change the number below to adjust the default width of the RAG/FAISS panel
  const [ragWidth, setRagWidth] = useState(340);
  const [isResizing, setIsResizing] = useState(false);
  const [leftWidth, setLeftWidth] = useState(320);
  const [isResizingLeft, setIsResizingLeft] = useState(false);

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
            const partial = event.current_state?.triage_result;
            if (partial) setFinalResult(partial);
            setStatus(prev => ({
              ...prev,
              extract: { active: false, complete: true, desc: '[LangChain] Extracting structured JSON.\nSummary created.' },
              duplicate_detection: { active: true, complete: false, desc: 'Searching FAISS vector DB...' },
            }));
          } else if (node === 'duplicate_detection') {
            const sim = event.current_state?.similar_reports || [];
            setSimilarReports(sim); // Update immediately during stream
            setStatus(prev => ({
              ...prev,
              duplicate_detection: {
                active: false, complete: true,
                desc: `[FAISS] Vector similarity search finished.\nMatched: ${sim.length}`,
              },
              triage: { active: true, complete: false, desc: 'Applying severity policies...' },
            }));
          } else if (node === 'triage') {
            const partial = event.current_state?.triage_result;
            if (partial) setFinalResult(partial);
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
      setError(e.message || 'Error connecting to backend API.');
    } finally {
      setIsRunning(false);
    }
  };

  const handleCommit = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/triage/commit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          bug_trace: bugTrace,
          user_review: userReview,
          triage_result: finalResult,
          similar_reports: similarReports,
          combined_text: combinedText
        }),
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
    <div style={{ display: 'flex', width: '100%', height: '100%' }}>
      {/* ── Left Panel (Resizable) ── */}
      <div style={{
        width: `${leftWidth}px`, backgroundColor: 'var(--surface)', borderRight: '1px solid var(--border)',
        padding: '20px', flexShrink: 0, overflowY: 'auto', display: 'flex', flexDirection: 'column'
      }}>

        {/* Form */}
        <div style={{ marginBottom: '32px' }}>
          <div style={{ marginBottom: '16px' }}>
            <label className="section-label" style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
              <Bug size={12} /> Bug Trace / Log Dump
            </label>
            <textarea
              className="code-input" rows={10}
              placeholder="Paste raw stack traces here..."
              value={bugTrace} onChange={e => setBugTrace(e.target.value)}
            />
          </div>
          <div style={{ marginBottom: '16px' }}>
            <label className="section-label" style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
              <MessageSquare size={12} /> User Review (Optional)
            </label>
            <textarea
              rows={3} placeholder="Additional context..."
              style={{ fontFamily: 'Inter, sans-serif' }}
              value={userReview} onChange={e => setUserReview(e.target.value)}
            />
          </div>
          <button className="btn-primary" onClick={runPipeline} disabled={isRunning || !bugTrace.trim()} style={{ width: '100%' }}>
            {isRunning ? <><Cpu size={14} className="status-pulsing" /> Running Analysis...</> : <><Play fill="white" size={14} /> Run Analysis</>}
          </button>
        </div>

        {error && (
          <div style={{ backgroundColor: 'var(--surface-alt)', border: '1px solid var(--error-red)', color: 'var(--error-red)', padding: '12px', borderRadius: '6px', fontSize: '13px', marginBottom: '24px' }}>
            {error}
          </div>
        )}

        {/* Pipeline Live Status */}
        <div style={{ paddingBottom: '24px' }}>
          <span className="section-label" style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '12px' }}>
            <Cpu size={12} /> Pipeline Status
          </span>
          <div>
            <StatusItem name="Preprocessing" s={status.preprocess} />
            <StatusItem name="Extraction" s={status.extract} />
            <StatusItem name="Duplicate Detection" s={status.duplicate_detection} />
            <StatusItem name="Triage" s={status.triage} />
          </div>

          {finalResult && (
            <div style={{ marginTop: '24px' }}>
              <button
                className="btn-primary"
                onClick={handleCommit}
                style={{ width: '100%', backgroundColor: 'var(--success-green)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
              >
                <Database size={14} /> Commit to Database
              </button>
            </div>
          )}
        </div>
      </div>

      {/* ── Left Drag Resizer ── */}
      <div
        onMouseDown={(e) => {
          e.preventDefault(); // prevent selection
          setIsResizingLeft(true);
          const startX = e.clientX;
          const startWidth = leftWidth;
          const onMouseMove = (moveEvent) => {
            const deltaX = moveEvent.clientX - startX; // moving right increases width
            const newWidth = Math.max(200, Math.min(800, startWidth + deltaX)); // clamp 200px - 800px
            setLeftWidth(newWidth);
          };
          const onMouseUp = () => {
            setIsResizingLeft(false);
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
          };
          document.addEventListener('mousemove', onMouseMove);
          document.addEventListener('mouseup', onMouseUp);
        }}
        onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--accent-primary)'}
        onMouseLeave={(e) => !isResizingLeft && (e.target.style.backgroundColor = 'transparent')}
        style={{
          width: '6px',
          cursor: 'col-resize',
          backgroundColor: isResizingLeft ? 'var(--accent-primary)' : 'transparent',
          zIndex: 10,
          transition: 'background-color 0.2s',
          flexShrink: 0
        }}
      />

      {/* ── Middle Panel (Triage Report) ── */}
      <div style={{
        flex: 1, backgroundColor: 'var(--surface)', padding: '24px', overflowY: 'auto'
      }}>
        {finalResult ? <TriageReportFilled result={finalResult} /> : <TriageReportEmpty />}
      </div>

      {/* ── Drag Resizer ── */}
      <div
        onMouseDown={(e) => {
          e.preventDefault(); // prevent text selection
          setIsResizing(true);
          const startX = e.clientX;
          const startWidth = ragWidth;
          const onMouseMove = (moveEvent) => {
            const deltaX = startX - moveEvent.clientX; // moving left increases width
            const newWidth = Math.max(200, Math.min(800, startWidth + deltaX)); // clamp 200px - 800px
            setRagWidth(newWidth);
          };
          const onMouseUp = () => {
            setIsResizing(false);
            document.removeEventListener('mousemove', onMouseMove);
            document.removeEventListener('mouseup', onMouseUp);
          };
          document.addEventListener('mousemove', onMouseMove);
          document.addEventListener('mouseup', onMouseUp);
        }}
        onMouseEnter={(e) => e.target.style.backgroundColor = 'var(--accent-primary)'}
        onMouseLeave={(e) => !isResizing && (e.target.style.backgroundColor = 'transparent')}
        style={{
          width: '6px',
          cursor: 'col-resize',
          backgroundColor: isResizing ? 'var(--accent-primary)' : 'transparent',
          zIndex: 10,
          transition: 'background-color 0.2s',
          flexShrink: 0
        }}
      />

      {/* ── Right Panel (RAG Sidebar) ── */}
      <div style={{
        width: `${ragWidth}px`, backgroundColor: 'var(--bg-parchment)', borderLeft: '1px solid var(--border)',
        padding: '16px', flexShrink: 0, overflowY: 'auto'
      }}>
        <div style={{ marginBottom: '20px' }}>
          <span className="section-label" style={{ display: 'block' }}>RAG Similarity · FAISS</span>
        </div>

        {!finalResult && (
          <p className="body-copy" style={{ color: 'var(--text-muted)', fontSize: '12px', fontStyle: 'italic' }}>Submit a report to see vectors.</p>
        )}

        {finalResult && similarReports.length === 0 && (
          <p className="body-copy" style={{ color: 'var(--text-muted)', fontSize: '12px' }}>No similar issues found.</p>
        )}

        {finalResult && similarReports.map((rep, i) => {
          const pct = (rep.similarity_score || 0) * 100;
          return <DuplicateCard key={i} index={i + 1} rep={rep} pct={pct} />;
        })}
      </div>

    </div>
  );
}
