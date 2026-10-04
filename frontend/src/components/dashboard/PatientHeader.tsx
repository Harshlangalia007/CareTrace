import React from 'react';
import type { Patient, ClinicalSummary } from '../../types';
import { Badge, StatusDot } from '../ui';

interface PatientHeaderProps {
  patient: Patient;
  summary?: ClinicalSummary;
  documentCount?: number;
  encounterCount?: number;
}

const PatientHeader: React.FC<PatientHeaderProps> = ({ patient, summary, documentCount, encounterCount }) => {
  const metaItems = [
    { label: 'Age', value: patient.age ? `${patient.age} years` : 'Unknown' },
    { label: 'Sex', value: patient.sex || 'Unknown' },
    { label: 'Admission', value: patient.current_admission || 'None active' },
    { label: 'Documents', value: documentCount ?? patient.document_count },
    { label: 'Encounters', value: encounterCount ?? patient.encounter_count },
  ];

  return (
    <div style={{
      background: 'var(--bg)', borderBottom: '1px solid var(--border)',
      padding: '20px 28px',
    }}>
      {/* Top row */}
      <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 24 }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 6 }}>
            <span style={{
              background: 'var(--surface-2)', border: '1px solid var(--border)',
              borderRadius: 'var(--radius)', padding: '3px 10px',
              fontSize: 12, fontWeight: 700, letterSpacing: '0.05em',
              fontFamily: 'var(--mono)', color: 'var(--text-muted)'
            }}>
              {patient.identifier}
            </span>
            <Badge variant="accent">Active Patient</Badge>
            {(summary?.conflicts_count ?? 0) > 0 && (
              <Badge variant="danger">
                {summary?.conflicts_count} Conflict{(summary?.conflicts_count ?? 0) !== 1 ? 's' : ''}
              </Badge>
            )}
            {(summary?.open_loops_count ?? 0) > 0 && (
              <Badge variant="warning">
                {summary?.open_loops_count} Open Loop{(summary?.open_loops_count ?? 0) !== 1 ? 's' : ''}
              </Badge>
            )}
          </div>

          {/* Major conditions */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginTop: 8 }}>
            {(summary?.conditions ?? patient.major_conditions.map(c => ({ name: c, status: 'active' }))).map((c, i) => (
              <span key={i} style={{
                background: 'var(--surface)', border: '1px solid var(--border)',
                borderRadius: 'var(--radius)', padding: '2px 10px',
                fontSize: 12, color: 'var(--text)',
                display: 'flex', alignItems: 'center', gap: 5,
              }}>
                <StatusDot status={c.status === 'active' ? 'red' : c.status === 'resolved' ? 'green' : 'yellow'} />
                {c.name}
              </span>
            ))}
          </div>
        </div>

        {/* Meta items */}
        <div style={{ display: 'flex', gap: 24, flexShrink: 0 }}>
          {metaItems.map(item => (
            <div key={item.label} style={{ textAlign: 'right' }}>
              <div style={{ fontSize: 11, color: 'var(--text-subtle)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: 2 }}>
                {item.label}
              </div>
              <div style={{ fontSize: 14, fontWeight: 600, color: 'var(--text)' }}>
                {String(item.value)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats bar */}
      {summary && (
        <div style={{
          display: 'flex', gap: 24, marginTop: 16,
          paddingTop: 14, borderTop: '1px solid var(--border)',
        }}>
          <StatChip label="Timeline Events" value={summary.timeline_events} />
          <StatChip label="Active Medications" value={summary.active_medications.length} />
          <StatChip label="Stopped Medications" value={summary.stopped_medications.length} variant="warning" />
          <StatChip label="Open Loops" value={summary.open_loops_count} variant="danger" />
          <StatChip label="Conflicts" value={summary.conflicts_count} variant="danger" />
          <StatChip label="Pending Investigations" value={summary.pending_investigations.length} variant="warning" />
        </div>
      )}
    </div>
  );
};

const StatChip: React.FC<{ label: string; value: number; variant?: 'default' | 'warning' | 'danger' }> = ({
  label, value, variant = 'default'
}) => {
  const colors = {
    default: { color: 'var(--text)' },
    warning: { color: 'var(--warning)' },
    danger: { color: 'var(--danger)' },
  };
  const { color } = colors[variant === 'default' || value === 0 ? 'default' : variant];

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <span style={{ fontSize: 18, fontWeight: 800, color: value > 0 ? color : 'var(--text-subtle)' }}>
        {value}
      </span>
      <span style={{ fontSize: 11, color: 'var(--text-subtle)', lineHeight: 1.3 }}>
        {label}
      </span>
    </div>
  );
};

export default PatientHeader;
