import React from 'react';
import type { ClinicalSummary, Condition, Medication, OpenLoop, Conflict, DetectedChange } from '../../types';
import { Card, SectionHeader, StatusDot, Badge } from '../ui';

interface ClinicalSnapshotProps {
  summary: ClinicalSummary;
  openLoops: OpenLoop[];
  conflicts: Conflict[];
  changes: DetectedChange[];
  conditions: Condition[];
  medications: Medication[];
  onViewLoops: () => void;
  onViewConflicts: () => void;
  onViewChanges: () => void;
}

const ClinicalSnapshot: React.FC<ClinicalSnapshotProps> = ({
  openLoops, conflicts, changes, conditions, medications,
  onViewLoops, onViewConflicts, onViewChanges
}) => {
  const activeMeds = medications.filter(m => m.status === 'active');
  const stoppedMeds = medications.filter(m => m.status === 'stopped');
  const activeConditions = conditions.filter(c => c.status === 'active');
  const recentChanges = changes.slice(0, 3);
  const topConflicts = conflicts.filter(c => !c.resolved).slice(0, 2);
  const topLoops = openLoops.filter(l => l.status === 'open').slice(0, 3);

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
      {/* Why This Patient Matters / Current State */}
      <Card>
        <SectionHeader title="Why This Patient Matters" />
        <p style={{ fontSize: 13, color: 'var(--text-muted)', lineHeight: 1.7, marginBottom: 16 }}>
          Complex multi-morbidity patient with{' '}
          <strong>{activeConditions.map(c => c.name).join(', ') || 'multiple conditions'}</strong>.
          Recent significant clinical events. Important medication changes and outstanding investigations
          require continuity of care.
        </p>
        <div style={{ borderTop: '1px solid var(--border)', paddingTop: 12, marginTop: 4 }}>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: '0.04em', textTransform: 'uppercase', color: 'var(--text-subtle)', marginBottom: 8 }}>
            Current State
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
            {activeMeds.length > 0 ? activeMeds.map(m => (
              <span key={m.id} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: '2px 8px', fontSize: 12, display: 'flex', alignItems: 'center', gap: 5 }}>
                <StatusDot status="green" />
                {m.name} {m.dose || ''}
              </span>
            )) : <span style={{ fontSize: 12, color: 'var(--text-subtle)' }}>No active medications found</span>}
            {stoppedMeds.map(m => (
              <span key={m.id} style={{ background: 'var(--danger-bg)', border: '1px solid var(--danger)', borderRadius: 'var(--radius)', padding: '2px 8px', fontSize: 12, color: 'var(--danger)', display: 'flex', alignItems: 'center', gap: 5 }}>
                <StatusDot status="red" />
                {m.name} — STOPPED
              </span>
            ))}
          </div>
        </div>
      </Card>

      {/* Recent Changes */}
      <Card>
        <SectionHeader
          title="Recent Changes"
          count={changes.length}
          actions={<button onClick={onViewChanges} style={{ fontSize: 12, color: 'var(--accent)', background: 'none', border: 'none', cursor: 'pointer' }}>View all →</button>}
        />
        {recentChanges.length === 0 ? (
          <p style={{ fontSize: 13, color: 'var(--text-subtle)' }}>No changes detected yet.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {recentChanges.map(ch => (
              <ChangeItem key={ch.id} change={ch} />
            ))}
          </div>
        )}
      </Card>

      {/* Open Loops */}
      <Card style={{ borderLeft: topLoops.length > 0 ? '3px solid var(--danger)' : undefined }}>
        <SectionHeader
          title="Open Loops"
          count={topLoops.length}
          actions={<button onClick={onViewLoops} style={{ fontSize: 12, color: 'var(--accent)', background: 'none', border: 'none', cursor: 'pointer' }}>View all →</button>}
        />
        {topLoops.length === 0 ? (
          <p style={{ fontSize: 13, color: 'var(--text-subtle)' }}>No open loops detected.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {topLoops.map(loop => (
              <LoopItem key={loop.id} loop={loop} />
            ))}
          </div>
        )}
      </Card>

      {/* Potential Conflicts */}
      <Card style={{ borderLeft: topConflicts.length > 0 ? '3px solid var(--warning)' : undefined }}>
        <SectionHeader
          title="Potential Conflicts"
          count={topConflicts.length}
          actions={<button onClick={onViewConflicts} style={{ fontSize: 12, color: 'var(--accent)', background: 'none', border: 'none', cursor: 'pointer' }}>View all →</button>}
        />
        {topConflicts.length === 0 ? (
          <p style={{ fontSize: 13, color: 'var(--text-subtle)' }}>No conflicts detected.</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
            {topConflicts.map(cf => (
              <ConflictItem key={cf.id} conflict={cf} />
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

const ChangeItem: React.FC<{ change: DetectedChange }> = ({ change }) => {
  const typeLabels: Record<string, string> = {
    medication_stopped: 'Medication Stopped',
    medication_started: 'Medication Started',
    dose_changed: 'Dose Changed',
    new_diagnosis: 'New Diagnosis',
    worsening: 'Worsening',
    improving: 'Improving',
    new_admission: 'New Admission',
    new_referral: 'New Referral',
  };

  return (
    <div style={{ borderLeft: '2px solid var(--border)', paddingLeft: 12 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 2 }}>
        <Badge variant={change.change_type === 'worsening' || change.change_type === 'medication_stopped' ? 'danger' : change.change_type === 'improving' ? 'success' : 'warning'}>
          {typeLabels[change.change_type] || change.change_type}
        </Badge>
        {change.entity_name && <span style={{ fontSize: 13, fontWeight: 600 }}>{change.entity_name}</span>}
      </div>
      {change.previous_state && change.current_state && (
        <div style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ textDecoration: 'line-through', color: 'var(--text-subtle)' }}>{change.previous_state}</span>
          <span>→</span>
          <span style={{ fontWeight: 600, color: 'var(--text)' }}>{change.current_state}</span>
        </div>
      )}
      {change.reason && <p style={{ fontSize: 11, color: 'var(--text-subtle)', marginTop: 2 }}>Reason: {change.reason}</p>}
    </div>
  );
};

const LoopItem: React.FC<{ loop: OpenLoop }> = ({ loop }) => (
  <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
    <span style={{ fontSize: 16, color: 'var(--danger)', flexShrink: 0, marginTop: 1 }}>●</span>
    <div>
      <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 2 }}>{loop.title}</div>
      {loop.description && <p style={{ fontSize: 12, color: 'var(--text-muted)', lineHeight: 1.5 }}>{loop.description.slice(0, 120)}{loop.description.length > 120 ? '…' : ''}</p>}
      <Badge variant="danger" size="sm">Potentially Outstanding</Badge>
    </div>
  </div>
);

const ConflictItem: React.FC<{ conflict: Conflict }> = ({ conflict }) => (
  <div style={{ display: 'flex', gap: 10, alignItems: 'flex-start' }}>
    <span style={{ fontSize: 16, color: 'var(--warning)', flexShrink: 0, marginTop: 1 }}>⚡</span>
    <div>
      <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 3 }}>{conflict.title}</div>
      <Badge variant={conflict.severity === 'high' ? 'danger' : 'warning'}>
        {conflict.severity.toUpperCase()} — Conflicting Documentation
      </Badge>
    </div>
  </div>
);

export default ClinicalSnapshot;
