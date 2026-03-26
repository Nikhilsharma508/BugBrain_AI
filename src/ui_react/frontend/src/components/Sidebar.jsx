import { NavLink } from 'react-router-dom';
import { Play, Activity } from 'lucide-react';
import { useSidebar } from '../context/SidebarContext';
import { motion, AnimatePresence } from 'framer-motion';

export default function Sidebar() {
  const { open } = useSidebar();

  return (
    <AnimatePresence initial={false}>
      {open && (
        <motion.aside
          key="sidebar"
          className="sidebar"
          initial={{ width: 0, opacity: 0 }}
          animate={{ width: 200, opacity: 1 }}
          exit={{ width: 0, opacity: 0 }}
          transition={{ type: 'spring', stiffness: 300, damping: 30 }}
          style={{ overflow: 'hidden' }}
        >
          <div className="sidebar-section-header">
            <span className="section-label">WORKSPACE</span>
          </div>

          <nav className="sidebar-nav">
            <NavLink
              to="/pipeline"
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              {({ isActive }) => (
                <>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                    <Play
                      size={14}
                      fill={isActive ? 'var(--accent-primary)' : 'none'}
                      stroke={isActive ? 'var(--accent-primary)' : 'currentColor'}
                    />
                    <span>Run Pipeline</span>
                  </div>
                  {isActive && <span className="live-badge">Live</span>}
                </>
              )}
            </NavLink>

            <NavLink
              to="/dashboard"
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Activity size={14} />
                <span>Dashboard</span>
              </div>
            </NavLink>
          </nav>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}
