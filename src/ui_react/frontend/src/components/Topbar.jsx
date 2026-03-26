import { Link, NavLink } from 'react-router-dom';
import { 
  ChevronDown, FileText, Book, ShieldAlert, Rocket, Settings,
  PanelLeftClose, PanelLeftOpen
} from 'lucide-react';
import { useSidebar } from '../context/SidebarContext';
import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import SettingsPanel from './SettingsPanel';

export default function Topbar() {
  const { open, toggle } = useSidebar();
  const [settingsOpen, setSettingsOpen] = useState(false);

  const docs = [
    { id: 'report', title: 'Submission Report', icon: <ShieldAlert size={14} /> },
    { id: 'system_guide', title: 'System Guide', icon: <Book size={14} /> },
    { id: 'readme', title: 'Project README', icon: <FileText size={14} /> },
    { id: 'migration_guide', title: 'UI Migration Guide', icon: <Rocket size={14} /> },
  ];

  return (
    <>
      <header className="topbar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {/* Sidebar toggle button */}
          <button
            onClick={toggle}
            style={{ color: 'var(--text-muted)', padding: '4px', display: 'flex' }}
            title={open ? 'Collapse sidebar' : 'Expand sidebar'}
          >
            {open ? <PanelLeftClose size={18} /> : <PanelLeftOpen size={18} />}
          </button>

          <div className="topbar-brand">
            TriageAI
            <div className="brand-dot" />
          </div>
        </div>

        <div className="topbar-actions">
          <div className="dropdown">
            <div className="topbar-link" style={{ display: 'flex', alignItems: 'center', gap: '4px', cursor: 'pointer' }}>
              Docs <ChevronDown size={14} />
            </div>
            <div className="dropdown-content">
              {docs.map(doc => (
                <Link key={doc.id} to={`/docs/${doc.id}`} className="dropdown-item">
                  {doc.icon}
                  {doc.title}
                </Link>
              ))}
            </div>
          </div>

          <button
            className="topbar-link"
            onClick={() => setSettingsOpen(true)}
            style={{ display: 'flex', alignItems: 'center', gap: '6px' }}
          >
            <Settings size={14} />
            Settings
          </button>

          <div className="user-avatar" />
        </div>
      </header>

      <AnimatePresence>
        {settingsOpen && <SettingsPanel onClose={() => setSettingsOpen(false)} />}
      </AnimatePresence>
    </>
  );
}
