import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface NavItem {
  label: string;
  path: string;
  icon?: string;
}

interface SidebarProps {
  currentPatientId?: string;
}

const globalNav: NavItem[] = [
  { label: 'Dashboard', path: '/', icon: '⊡' },
  { label: 'Patients', path: '/patients', icon: '◎' },
];

const patientNav = (id: string): NavItem[] => [
  { label: 'Overview', path: `/patient/${id}`, icon: '▦' },
  { label: 'Timeline', path: `/patient/${id}/timeline`, icon: '↓' },
  { label: 'What Changed?', path: `/patient/${id}/changes`, icon: '⟳' },
  { label: 'Open Loops', path: `/patient/${id}/loops`, icon: '○' },
  { label: 'Conflicts', path: `/patient/${id}/conflicts`, icon: '⚡' },
  { label: 'Evidence', path: `/patient/${id}/evidence`, icon: '◈' },
  { label: 'Documents', path: `/patient/${id}/documents`, icon: '◻' },
];

const generateNav = (id: string): NavItem[] => [
  { label: 'Next Clinician Brief', path: `/patient/${id}/brief`, icon: '★' },
  { label: 'Ward Round', path: `/patient/${id}/ward-round`, icon: '♦' },
  { label: 'Referral', path: `/patient/${id}/referral`, icon: '→' },
  { label: 'Discharge', path: `/patient/${id}/discharge`, icon: '↗' },
];

const NavSection: React.FC<{ title?: string; items: NavItem[]; location: string }> = ({
  title, items, location
}) => (
  <div style={{ marginBottom: 24 }}>
    {title && (
      <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--text-subtle)', padding: '0 16px 8px' }}>
        {title}
      </div>
    )}
    {items.map(item => {
      const active = location === item.path || (item.path !== '/' && location.startsWith(item.path));
      return (
        <Link
          key={item.path}
          to={item.path}
          style={{
            display: 'flex', alignItems: 'center', gap: 10,
            padding: '7px 16px', fontSize: 13, fontWeight: active ? 600 : 400,
            color: active ? 'var(--text)' : 'var(--text-muted)',
            background: active ? 'var(--surface-2)' : 'transparent',
            borderLeft: active ? '2px solid var(--text)' : '2px solid transparent',
            textDecoration: 'none', transition: 'all 0.1s',
            marginLeft: -1,
          }}
        >
          <span style={{ fontSize: 12, width: 16, flexShrink: 0, textAlign: 'center' }}>{item.icon}</span>
          {item.label}
        </Link>
      );
    })}
  </div>
);

const Sidebar: React.FC<SidebarProps> = ({ currentPatientId }) => {
  const location = useLocation();

  return (
    <nav style={{
      width: 224,
      flexShrink: 0,
      background: 'var(--bg)',
      borderRight: '1px solid var(--border)',
      height: '100vh',
      position: 'sticky',
      top: 0,
      overflow: 'auto',
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Logo */}
      <div style={{ padding: '20px 16px 16px', borderBottom: '1px solid var(--border)', marginBottom: 16 }}>
        <div style={{ fontSize: 18, fontWeight: 800, letterSpacing: '-0.5px', color: 'var(--text)' }}>
          THREAD
        </div>
        <div style={{ fontSize: 10, color: 'var(--text-subtle)', letterSpacing: '0.08em', textTransform: 'uppercase', marginTop: 2 }}>
          Clinical Continuity Engine
        </div>
      </div>

      <NavSection items={globalNav} location={location.pathname} />

      {currentPatientId && (
        <>
          <div style={{ borderTop: '1px solid var(--border)', marginBottom: 16, marginTop: 4 }} />
          <NavSection title="Current Patient" items={patientNav(currentPatientId)} location={location.pathname} />
          <div style={{ borderTop: '1px solid var(--border)', marginBottom: 16, marginTop: 4 }} />
          <NavSection title="Generate" items={generateNav(currentPatientId)} location={location.pathname} />
        </>
      )}

      {/* Bottom info */}
      <div style={{ marginTop: 'auto', padding: '16px', borderTop: '1px solid var(--border)', fontSize: 11, color: 'var(--text-subtle)' }}>
        IBM Bob Hackathon × VGEC
      </div>
    </nav>
  );
};

export default Sidebar;
