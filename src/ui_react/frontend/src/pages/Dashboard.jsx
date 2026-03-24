import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { BarChart3, Zap, Wrench, Dna, ClipboardList } from 'lucide-react';
import GlassCard from '../components/GlassCard';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/dashboard')
      .then(r => r.json())
      .then(d => {
        setData(d);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <h2 style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '5rem' }}>Loading Analytics...</h2>;
  }

  if (!data || data.status === 'empty') {
    return (
      <GlassCard style={{ textAlign: 'center', marginTop: '2rem' }}>
        <h3 style={{ color: 'var(--text-secondary)' }}>No Data Found</h3>
        <p style={{ color: 'var(--text-secondary)' }}>Run the triage pipeline to generate analytics.</p>
      </GlassCard>
    );
  }

  const { metrics, severity_counts, team_counts, error_patterns, recent_reports } = data;

  const sevData = Object.entries(severity_counts).map(([name, val]) => ({ name, value: val }));
  const teamData = Object.entries(team_counts).map(([name, val]) => ({ name, value: val }));

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <h1 style={{ color: 'var(--text-accent)', textAlign: 'center', fontSize: '3rem', margin: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '15px' }}>
        <BarChart3 size={48} /> TRIAGE ANALYTICS
      </h1>
      <p style={{ color: 'var(--text-secondary)', textAlign: 'center', marginBottom: '3rem', fontSize: '1.1rem' }}>
        // REAL-TIME SYSTEM PERFORMANCE DASHBOARD //
      </p>

      {/* TOP METRICS */}
      <div className="grid-4-col" style={{ marginBottom: '2rem' }}>
        <GlassCard style={{ textAlign: 'center' }}>
          <div style={{ color: 'var(--text-accent)', fontSize: '2.5rem', fontWeight: 800 }}>{metrics.total_reports}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 600, textTransform: 'uppercase' }}>Reports Handled</div>
        </GlassCard>
        <GlassCard style={{ textAlign: 'center' }}>
          <div style={{ color: '#ff9999', fontSize: '2.5rem', fontWeight: 800 }}>{metrics.top_severity}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 600, textTransform: 'uppercase' }}>Main Impact</div>
        </GlassCard>
        <GlassCard style={{ textAlign: 'center' }}>
          <div style={{ color: '#99ff99', fontSize: '2.5rem', fontWeight: 800 }}>{metrics.top_owner}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 600, textTransform: 'uppercase' }}>Lead Assignee</div>
        </GlassCard>
        <GlassCard style={{ textAlign: 'center' }}>
          <div style={{ color: 'var(--text-accent)', fontSize: '2.5rem', fontWeight: 800 }}>{metrics.avg_summary_length}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', fontWeight: 600, textTransform: 'uppercase' }}>Avg Summary Length</div>
        </GlassCard>
      </div>

      {/* CHARTS */}
      <div className="grid-2-col" style={{ marginBottom: '2rem' }}>
        <GlassCard>
          <h3 style={{ color: '#90c4f0', textTransform: 'uppercase', letterSpacing: '2.5px', marginBottom: '1.5rem', fontSize: '1.05rem', borderBottom: '1px solid rgba(100,182,255,0.4)', paddingBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Zap size={20} color="#ffc107" /> Severity Spread
          </h3>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sevData}>
                <XAxis dataKey="name" stroke="var(--text-secondary)" />
                <YAxis stroke="var(--text-secondary)" allowDecimals={false} />
                <Tooltip cursor={{ fill: 'rgba(100, 182, 255, 0.1)' }} contentStyle={{ background: 'var(--glass-bg)', border: '1px solid var(--text-accent)', borderRadius: '8px' }} />
                <Bar dataKey="value" fill="#64b6ff" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <GlassCard>
          <h3 style={{ color: '#90c4f0', textTransform: 'uppercase', letterSpacing: '2.5px', marginBottom: '1.5rem', fontSize: '1.05rem', borderBottom: '1px solid rgba(100,182,255,0.4)', paddingBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Wrench size={20} color="#a855f7" /> Team Load
          </h3>
          <div style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teamData}>
                <XAxis dataKey="name" stroke="var(--text-secondary)" />
                <YAxis stroke="var(--text-secondary)" allowDecimals={false} />
                <Tooltip cursor={{ fill: 'rgba(100, 182, 255, 0.1)' }} contentStyle={{ background: 'var(--glass-bg)', border: '1px solid #a855f7', borderRadius: '8px' }} />
                <Bar dataKey="value" fill="#a855f7" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>
      </div>

      {/* TABLES */}
      <GlassCard style={{ marginBottom: '2rem' }}>
        <h3 style={{ color: 'var(--text-primary)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Dna size={20} color="#64b6ff" /> ERROR PATTERN RECOGNITION
        </h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(100,150,220,0.3)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.5rem' }}>Error Type</th>
              <th style={{ padding: '0.5rem' }}>Frequency</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(error_patterns).map(([err, freq], i) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(100,150,220,0.1)' }}>
                <td style={{ padding: '0.5rem' }}>{err}</td>
                <td style={{ padding: '0.5rem' }}>{freq}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>

      <GlassCard>
        <h3 style={{ color: 'var(--text-primary)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ClipboardList size={20} color="#64b6ff" /> RECENT CLASSIFICATIONS
        </h3>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid rgba(100,150,220,0.3)', color: 'var(--text-secondary)' }}>
              <th style={{ padding: '0.5rem' }}>ID</th>
              <th style={{ padding: '0.5rem' }}>Severity</th>
              <th style={{ padding: '0.5rem' }}>Owner</th>
              <th style={{ padding: '0.5rem' }}>Summary</th>
              <th style={{ padding: '0.5rem' }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {recent_reports.map((rep, i) => (
              <tr key={i} style={{ borderBottom: '1px solid rgba(100,150,220,0.1)' }}>
                <td style={{ padding: '0.5rem', color: 'var(--text-accent)' }}>{rep.Id}</td>
                <td style={{ padding: '0.5rem', color: '#ff9800' }}>{rep.Severity}</td>
                <td style={{ padding: '0.5rem' }}>{rep.Owner}</td>
                <td style={{ padding: '0.5rem' }}>{rep.Summary}</td>
                <td style={{ padding: '0.5rem', color: 'var(--text-secondary)' }}>{rep.Timestamp}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>
    </motion.div>
  );
}
