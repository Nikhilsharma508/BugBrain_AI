import { useState, useEffect, useRef } from 'react';
import { useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion, useScroll, useSpring } from 'framer-motion';
import { Eye, Edit3, Save, Loader2, CheckCircle2 } from 'lucide-react';

export default function DocsViewer() {
  const { filename } = useParams();
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState('view'); // 'view' or 'edit'
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [displayName, setDisplayName] = useState('');

  // Scroll progress tracking
  const scrollContainerRef = useRef(null);
  const { scrollYProgress } = useScroll({ container: scrollContainerRef });
  const scaleX = useSpring(scrollYProgress, { stiffness: 200, damping: 30 });

  useEffect(() => {
    fetchDoc();
    setMode('view');
    setSaved(false);
  }, [filename]);

  const fetchDoc = async () => {
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/api/docs/${filename}`);
      const data = await res.json();
      setContent(data.content);
      setDisplayName(data.filename);
    } catch (e) {
      console.error("Failed to fetch doc:", e);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await fetch(`http://localhost:8000/api/docs/${filename}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
      });
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      setMode('view');
    } catch (e) {
      alert("Failed to save: " + e.message);
    } finally {
      setSaving(false);
    }
  };

  // Custom components for ReactMarkdown
  const components = {
    img: ({ node, ...props }) => {
      let { src } = props;
      // If it's a relative path starting with images/, proxy it through our API
      if (src && src.startsWith('images/')) {
        src = `http://localhost:8000/api/docs/image/${src}`;
      }
      return <img {...props} src={src} style={{ maxWidth: '100%', borderRadius: '8px', border: '1px solid var(--border)', margin: '16px 0' }} />;
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <Loader2 className="status-pulsing" size={32} color="var(--accent-primary)" />
      </div>
    );
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', backgroundColor: 'var(--surface)', overflow: 'hidden' }}>
      {/* Header bar */}
      <div style={{ 
        height: '56px', borderBottom: '1px solid var(--border)', padding: '0 24px',
        display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexShrink: 0
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <span style={{ fontFamily: 'JetBrains Mono', fontSize: '12px', color: 'var(--text-muted)' }}>Docs / {displayName}</span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {saved && <span style={{ color: 'var(--success-green)', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '4px' }}><CheckCircle2 size={14} /> Saved</span>}
          
          <div style={{ display: 'flex', backgroundColor: 'var(--surface-alt)', borderRadius: '6px', padding: '2px' }}>
            <button 
              onClick={() => setMode('view')}
              style={{ 
                padding: '6px 12px', borderRadius: '4px', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px',
                backgroundColor: mode === 'view' ? 'var(--surface)' : 'transparent',
                color: mode === 'view' ? 'var(--text-primary)' : 'var(--text-muted)',
                boxShadow: mode === 'view' ? '0 1px 2px rgba(0,0,0,0.05)' : 'none'
              }}
            >
              <Eye size={14} /> View
            </button>
            <button 
              onClick={() => setMode('edit')}
              style={{ 
                padding: '6px 12px', borderRadius: '4px', fontSize: '12px', display: 'flex', alignItems: 'center', gap: '6px',
                backgroundColor: mode === 'edit' ? 'var(--surface)' : 'transparent',
                color: mode === 'edit' ? 'var(--text-primary)' : 'var(--text-muted)',
                boxShadow: mode === 'edit' ? '0 1px 2px rgba(0,0,0,0.05)' : 'none'
              }}
            >
              <Edit3 size={14} /> Edit
            </button>
          </div>

          {mode === 'edit' && (
            <button 
              onClick={handleSave} 
              disabled={saving}
              className="btn-primary" 
              style={{ height: '32px', padding: '0 12px', fontSize: '12px' }}
            >
              {saving ? <Loader2 size={14} className="status-pulsing" /> : <Save size={14} />}
              Save Changes
            </button>
          )}
        </div>
      </div>

      {/* Reading progress bar — tracks scroll within the content area below */}
      <motion.div
        style={{
          scaleX,
          transformOrigin: '0%',
          height: '3px',
          backgroundColor: 'var(--accent-primary)',
          flexShrink: 0
        }}
      />

      {/* Content Area */}
      <div ref={scrollContainerRef} style={{ flex: 1, overflowY: 'auto', padding: '40px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {mode === 'view' ? (
            <div className="markdown-body">
              <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
                {content}
              </ReactMarkdown>
            </div>
          ) : (
            <textarea 
              className="code-input"
              style={{ minHeight: 'calc(100vh - 200px)', width: '100%', border: 'none', background: 'transparent' }}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Write markdown here..."
            />
          )}
        </div>
      </div>
    </div>
  );
}

