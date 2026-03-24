import { NavLink } from 'react-router-dom';
import { LayoutDashboard, BugPlay } from 'lucide-react';

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2 style={{ fontSize: '1.5rem', margin: 0, color: 'var(--text-accent)' }}>🐛 AI Bug Triage</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
          Intelligent parsing & routing
        </p>
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/pipeline"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <BugPlay size={20} />
          Run Triage Pipeline
        </NavLink>

        <NavLink
          to="/dashboard"
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <LayoutDashboard size={20} />
          Dashboard Analytics
        </NavLink>
      </nav>
    </aside>
  );
}
