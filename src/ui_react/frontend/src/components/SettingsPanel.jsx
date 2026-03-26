import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  SlidersHorizontal, X, Save, RotateCcw, Loader2,
  CheckCircle2, Info
} from 'lucide-react';

// Runtime CSS Variable overrides (temporary, resets on refresh)
const CSS_META = {
  '--accent-primary': { label: 'Accent Colour', type: 'color', default: '#C47A3A' },
  '--bg-parchment': { label: 'Background', type: 'color', default: '#F5F0E8' },
  '--surface': { label: 'Surface', type: 'color', default: '#FAF7F2' },
  '--text-primary': { label: 'Text Colour', type: 'color', default: '#1A1612' },
};

export default function SettingsPanel({ onClose }) {
  const [cssValues, setCssValues] = useState({});
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('css');

  useEffect(() => {
    // Read current CSS variables
    const root = document.documentElement;
    const css = {};
    Object.keys(CSS_META).forEach(k => {
      css[k] = getComputedStyle(root).getPropertyValue(k).trim() || CSS_META[k].default;
    });
    setCssValues(css);
  }, []);

  const handleCssChange = (key, val) => {
    setCssValues(prev => ({ ...prev, [key]: val }));
    document.documentElement.style.setProperty(key, val);
  };

  const handleResetCss = () => {
    Object.entries(CSS_META).forEach(([k, meta]) => {
      document.documentElement.style.setProperty(k, meta.default);
    });
    const reset = {};
    Object.keys(CSS_META).forEach(k => { reset[k] = CSS_META[k].default; });
    setCssValues(reset);
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      style={{
        position: 'fixed', inset: 0, backgroundColor: 'rgba(26,22,18,0.4)',
        zIndex: 200, display: 'flex', alignItems: 'flex-start', justifyContent: 'flex-end'
      }}
      onClick={onClose}
    >
      <motion.div
        initial={{ x: '100%' }}
        animate={{ x: 0 }}
        exit={{ x: '100%' }}
        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
        onClick={e => e.stopPropagation()}
        style={{
          width: '400px', height: '100vh', backgroundColor: 'var(--surface)',
          borderLeft: '1px solid var(--border)', display: 'flex', flexDirection: 'column'
        }}
      >
        {/* Header */}
        <div style={{ 
          height: '56px', display: 'flex', alignItems: 'center', justifyContent: 'space-between',
          padding: '0 20px', borderBottom: '1px solid var(--border)', flexShrink: 0
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <SlidersHorizontal size={16} color="var(--accent-primary)" />
            <span style={{ fontWeight: 600, fontSize: '13px' }}>System Settings</span>
          </div>
          <button onClick={onClose} style={{ color: 'var(--text-muted)', padding: '4px' }}>
            <X size={16} />
          </button>
        </div>

        {/* Tabs */}
        <div style={{ display: 'flex', borderBottom: '1px solid var(--border)', flexShrink: 0 }}>
          <button
            style={{
              flex: 1, padding: '12px', fontSize: '12px', fontWeight: 500,
              borderBottom: '2px solid var(--accent-primary)',
              color: 'var(--accent-primary)',
            }}
          >
            Appearance
          </button>
        </div>

        {/* Content */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '20px' }}>
          {loading ? (
            <div style={{ textAlign: 'center', paddingTop: '40px' }}>
              <Loader2 size={24} className="status-pulsing" color="var(--accent-primary)" />
            </div>
          ) : (
            <div>
              <div style={{ 
                backgroundColor: 'var(--team-blue-bg)', border: '1px solid var(--team-blue-border)',
                borderRadius: '6px', padding: '10px 12px', marginBottom: '20px',
                display: 'flex', gap: '8px', fontSize: '12px', color: 'var(--team-blue-text)'
              }}>
                <Info size={14} style={{ flexShrink: 0, marginTop: '1px' }} />
                Appearance changes are temporary and reset on page refresh.
              </div>
              {Object.entries(CSS_META).map(([key, meta]) => (
                <div key={key} style={{ marginBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '13px', color: 'var(--text-primary)' }}>{meta.label}</span>
                  <input
                    type="color"
                    value={cssValues[key] || meta.default}
                    onChange={e => handleCssChange(key, e.target.value)}
                    style={{ width: '40px', height: '32px', border: '1px solid var(--border)', borderRadius: '6px', cursor: 'pointer' }}
                  />
                </div>
              ))}
              <button
                onClick={handleResetCss}
                style={{ 
                  display: 'flex', alignItems: 'center', gap: '6px',
                  color: 'var(--text-muted)', fontSize: '12px', marginTop: '8px'
                }}
              >
                <RotateCcw size={12} /> Reset to defaults
              </button>
            </div>
          )}
        </div>


      </motion.div>
    </motion.div>
  );
}
