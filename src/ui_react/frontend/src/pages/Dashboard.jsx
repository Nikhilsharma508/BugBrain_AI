import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { motion } from 'framer-motion';
import {
  BarChart3, Activity, ShieldAlert, Users,
  FileSearch, AlertCircle, Database, History,
  TrendingUp, Clock
} from 'lucide-react';

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
    return (
      <div style={{ display: 'flex', flex: 1, alignItems: 'center', justifyContent: 'center' }}>
        <div className="status-pulsing" style={{ width: 40, height: 40, borderRadius: '50%', backgroundColor: 'var(--accent-primary)' }} />
      </div>
    );
  }

  if (!data || data.status === 'empty') {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <div style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', padding: '40px', borderRadius: '12px', maxWidth: '500px', margin: '0 auto' }}>
          <Database size={48} color="var(--text-muted)" style={{ marginBottom: '16px' }} />
          <h3 style={{ color: 'var(--text-primary)', marginBottom: '8px' }}>No Data Found</h3>
          <p style={{ color: 'var(--text-secondary)' }}>Run the triage pipeline to generate analytics.</p>
        </div>
      </div>
    );
  }

  const { metrics, severity_counts, team_counts, error_patterns, recent_reports } = data;
  const sevData = Object.entries(severity_counts).map(([name, val]) => ({ name, value: val }));
  // Sort team data by count descending
  const teamData = Object.entries(team_counts)
    .map(([name, val]) => ({ name, value: val }))
    .sort((a, b) => b.value - a.value);

  return (
    <div style={{ padding: '32px', maxWidth: '1400px', margin: '0 auto', minHeight: '100%' }}>
      <header style={{ marginBottom: '40px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
          <Activity size={20} color="var(--accent-primary)" />
          <span className="section-label">System Performance</span>
        </div>
        <h1 style={{ fontSize: '24px', color: 'var(--text-primary)' }}>Triage Dashboard</h1>
      </header>

      {/* TOP METRICS */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px', marginBottom: '32px' }}>
        {[
          { label: 'Total Reports', val: metrics.total_reports, icon: <FileSearch size={18} />, color: 'var(--accent-primary)' },
          { label: 'Main Impact', val: metrics.top_severity, icon: <ShieldAlert size={18} />, color: 'var(--error-red)' },
          { label: 'Lead Assignee', val: metrics.top_owner, icon: <Users size={18} />, color: 'var(--team-blue-text)' },
        ].map((m, i) => (
          <div key={i} style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', padding: '20px', borderRadius: '8px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', color: 'var(--text-muted)' }}>
              {m.icon}
              <span style={{ fontSize: '11px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.04em' }}>{m.label}</span>
            </div>
            <div style={{ fontSize: '24px', fontWeight: 600, color: m.color }}>{m.val}</div>
          </div>
        ))}
      </div>

      {/* CHARTS */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px', marginBottom: '32px' }}>
        <div style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', padding: '24px', borderRadius: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
            <div className="brand-dot" />
            <span className="section-label">Severity Spread</span>
          </div>
          <div style={{ height: 260 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={sevData}>
                <XAxis dataKey="name" axisLine={false} tickLine={false} style={{ fontSize: '11px', fill: 'var(--text-muted)' }} />
                <Tooltip cursor={{ fill: 'var(--surface-alt)' }} contentStyle={{ border: '1px solid var(--border)', borderRadius: '6px' }} />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {sevData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.name.includes('P1') ? 'var(--error-red)' : 'var(--accent-primary)'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', padding: '24px', borderRadius: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}>
            <div className="brand-dot" />
            <span className="section-label">Team Distribution</span>
          </div>
          <div style={{ height: 320 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={teamData} margin={{ bottom: 60 }}>
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  interval={0}
                  angle={-45}
                  textAnchor="end"
                  style={{ fontSize: '10px', fill: 'var(--text-muted)' }} 
                />
                <Tooltip cursor={{ fill: 'var(--surface-alt)' }} contentStyle={{ border: '1px solid var(--border)', borderRadius: '6px' }} />
                <Bar dataKey="value" fill="var(--team-blue-text)" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* TABLES */}
      <div style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', marginBottom: '32px', overflow: 'hidden' }}>
        <div style={{ padding: '20px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <AlertCircle size={18} color="var(--accent-primary)" />
          <span className="section-label" style={{ color: 'var(--text-primary)' }}>Error Pattern Recognition</span>
        </div>
        {/* Fixed-height scrollable table */}
        <div style={{ maxHeight: '240px', overflowY: 'auto', padding: '0 20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border)' }}>
                <th style={{ padding: '16px 0', fontWeight: 500, color: 'var(--text-muted)' }}>Error Signature</th>
                <th style={{ padding: '16px 0', fontWeight: 500, color: 'var(--text-muted)', textAlign: 'right' }}>Frequency</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(error_patterns).map(([err, freq], i) => (
                <tr key={i} style={{ borderBottom: i === Object.keys(error_patterns).length - 1 ? 'none' : '1px solid var(--surface-alt)' }}>
                  <td style={{ padding: '12px 0', fontFamily: 'JetBrains Mono, monospace', fontSize: '12px', color: 'var(--text-secondary)' }}>{err}</td>
                  <td style={{ padding: '12px 0', textAlign: 'right', fontWeight: 600, color: 'var(--accent-primary)' }}>{freq}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{ backgroundColor: 'var(--surface)', border: '1px solid var(--border)', borderRadius: '8px', overflow: 'hidden' }}>
        <div style={{ padding: '20px', borderBottom: '1px solid var(--border)', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <History size={18} color="var(--accent-primary)" />
          <span className="section-label" style={{ color: 'var(--text-primary)' }}>Recent Classifications</span>
        </div>
        {/* Fixed-height scrollable table — shows last ~6 rows then scrolls horizontally + vertically */}
        <div style={{ maxHeight: '320px', overflowY: 'auto', overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
            <thead>
              <tr style={{ textAlign: 'left', borderBottom: '1px solid var(--border)' }}>
                <th style={{ padding: '16px 20px', fontWeight: 500, color: 'var(--text-muted)' }}>ID</th>
                <th style={{ padding: '16px 20px', fontWeight: 500, color: 'var(--text-muted)' }}>Priority</th>
                <th style={{ padding: '16px 20px', fontWeight: 500, color: 'var(--text-muted)' }}>Owner</th>
                <th style={{ padding: '16px 20px', fontWeight: 500, color: 'var(--text-muted)' }}>Summary</th>
                <th style={{ padding: '16px 20px', fontWeight: 500, color: 'var(--text-muted)', textAlign: 'right' }}>Date</th>
              </tr>
            </thead>
            <tbody>
              {recent_reports.map((rep, i) => (
                <tr key={i} style={{ borderBottom: '1px solid var(--surface-alt)' }}>
                  <td style={{ padding: '12px 20px', fontWeight: 600, color: 'var(--text-primary)' }}>{rep.Id}</td>
                  <td style={{ padding: '12px 20px' }}>
                    <span style={{
                      padding: '2px 8px', borderRadius: '4px', fontSize: '11px', fontWeight: 600,
                      backgroundColor: rep.Severity?.includes('P1') ? 'var(--error-red)' : 'var(--sev-amber-bg)',
                      color: rep.Severity?.includes('P1') ? 'white' : 'var(--sev-amber-text)'
                    }}>
                      {rep.Severity}
                    </span>
                  </td>
                  <td style={{ padding: '12px 20px', color: 'var(--text-secondary)' }}>{rep.Owner}</td>
                  <td style={{ padding: '12px 20px', color: 'var(--text-secondary)', maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>{rep.Summary}</td>
                  <td style={{ padding: '12px 20px', textAlign: 'right', color: 'var(--text-muted)', fontSize: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '4px' }}>
                      <Clock size={12} /> {rep.Timestamp}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
