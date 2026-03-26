import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import Topbar from './components/Topbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import TriagePipeline from './pages/TriagePipeline';
import DocsViewer from './pages/DocsViewer';
import { SidebarProvider } from './context/SidebarContext';

// Page transition variants
const pageVariants = {
  initial: { opacity: 0, y: 12 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.25, ease: 'easeOut' } },
  exit: { opacity: 0, y: -8, transition: { duration: 0.15, ease: 'easeIn' } },
};

function AnimatedRoutes() {
  const location = useLocation();
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={location.pathname}
        variants={pageVariants}
        initial="initial"
        animate="animate"
        exit="exit"
        style={{ display: 'flex', flexDirection: 'column', flex: 1, minHeight: '100%' }}
      >
        <Routes location={location}>
          <Route path="/" element={<Navigate to="/pipeline" replace />} />
          <Route path="/pipeline" element={<TriagePipeline />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/docs/:filename" element={<DocsViewer />} />
        </Routes>
      </motion.div>
    </AnimatePresence>
  );
}

function App() {
  return (
    <SidebarProvider>
      <div className="app-container">
        <Topbar />
        <div className="app-main-flex">
          <Sidebar />
          <main className="main-content">
            <AnimatedRoutes />
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}

export default App;
