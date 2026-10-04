import React, { useState } from 'react';
import { format, parseISO } from 'date-fns';
import type { TimelineEvent } from '../../types';
import { SourceBadge, EmptyState } from '../ui';

interface ClinicalTimelineProps {
  events: TimelineEvent[];
  onSelectEvent?: (event: TimelineEvent) => void;
}

const eventTypeConfig: Record<string, { label: string; color: string; bg: string; icon: string }> = {
  admission: { label: 'Admission', color: 'var(--danger)', bg: 'var(--danger-bg)', icon: '⬤' },
  discharge: { label: 'Discharge', color: 'var(--success)', bg: 'var(--success-bg)', icon: '◎' },
  diagnosis: { label: 'Diagnosis', color: 'var(--purple)', bg: 'var(--purple-bg)', icon: '◈' },
  medication_start: { label: 'Med Started', color: 'var(--accent)', bg: 'var(--accent-bg)', icon: '+' },
  medication_stop: { label: 'Med Stopped', color: 'var(--danger)', bg: 'var(--danger-bg)', icon: '−' },
  medication_change: { label: 'Med Changed', color: 'var(--warning)', bg: 'var(--warning-bg)', icon: '⟳' },
  investigation: { label: 'Investigation', color: 'var(--text-muted)', bg: 'var(--surface-2)', icon: '◻' },
  result: { label: 'Result', color: 'var(--text-muted)', bg: 'var(--surface)', icon: '◦' },
  referral: { label: 'Referral', color: 'var(--purple)', bg: 'var(--purple-bg)', icon: '→' },
  follow_up: { label: 'Follow-up', color: 'var(--warning)', bg: 'var(--warning-bg)', icon: '⏱' },
  procedure: { label: 'Procedure', color: 'var(--text)', bg: 'var(--surface-2)', icon: '▤' },
  consultation: { label: 'Consultation', color: 'var(--text-muted)', bg: 'var(--surface)', icon: '◉' },
  allergy: { label: 'Allergy', color: 'var(--danger)', bg: 'var(--danger-bg)', icon: '⚠' },
  other: { label: 'Event', color: 'var(--text-subtle)', bg: 'var(--surface)', icon: '·' },
};

function getMonthGroup(dateStr?: string): string {
  if (!dateStr) return 'Unknown Date';
  try {
    return format(parseISO(dateStr), 'MMM yyyy');
  } catch {
    return 'Unknown Date';
  }
}

function formatDate(dateStr?: string): string {
  if (!dateStr) return '';
  try {
    return format(parseISO(dateStr), 'dd MMM yyyy');
  } catch {
    return '';
  }
}

function significanceBorder(sig?: string) {
  if (sig === 'high') return '2px solid var(--danger)';
  if (sig === 'medium') return '1px solid var(--border)';
  return '1px solid var(--border)';
}

const ClinicalTimeline: React.FC<ClinicalTimelineProps> = ({ events, onSelectEvent }) => {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (events.length === 0) {
    return <EmptyState icon="↓" title="No timeline events" subtitle="Upload and process patient documents to build the clinical timeline." />;
  }

  // Group by month
  const grouped: Record<string, TimelineEvent[]> = {};
  for (const evt of events) {
    const key = getMonthGroup(evt.event_date);
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(evt);
  }

  const months = Object.keys(grouped);

  return (
    <div style={{ position: 'relative', paddingLeft: 24 }}>
      {/* Vertical line */}
      <div style={{
        position: 'absolute', left: 11, top: 0, bottom: 0,
        width: 2, background: 'var(--border)',
      }} />

      {months.map((month) => (
        <div key={month} style={{ marginBottom: 8 }}>
          {/* Month label */}
          <div style={{
            position: 'relative', display: 'flex', alignItems: 'center', gap: 10,
            marginBottom: 12, marginLeft: -24,
          }}>
            <div style={{
              width: 24, height: 24, borderRadius: '50%',
              background: 'var(--text)', display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0,
            }} />
            <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text)', letterSpacing: '-0.01em' }}>
              {month}
            </span>
          </div>

          {/* Events */}
          {grouped[month].map((evt) => {
            const config = eventTypeConfig[evt.event_type] || eventTypeConfig.other;
            const isSelected = selectedId === evt.id;
            const isExpanded = expandedId === evt.id;

            return (
              <div key={evt.id} style={{ position: 'relative', marginBottom: 10, marginLeft: 4 }}>
                {/* Dot */}
                <div style={{
                  position: 'absolute', left: -18, top: 12,
                  width: 10, height: 10, borderRadius: '50%',
                  background: config.color,
                  border: '2px solid var(--bg)',
                  zIndex: 1,
                }} />

                {/* Card */}
                <div
                  onClick={() => {
                    const newId = isExpanded ? null : evt.id;
                    setExpandedId(newId);
                    setSelectedId(evt.id);
                    onSelectEvent?.(evt);
                  }}
                  style={{
                    background: 'var(--bg)',
                    border: isSelected ? `2px solid ${config.color}` : significanceBorder(evt.clinical_significance),
                    borderRadius: 'var(--radius-lg)',
                    padding: '12px 16px',
                    cursor: 'pointer',
                    transition: 'border-color 0.15s',
                    boxShadow: isSelected ? `0 0 0 3px ${config.bg}` : 'var(--shadow)',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{
                        width: 22, height: 22, borderRadius: 'var(--radius)',
                        background: config.bg, color: config.color,
                        display: 'flex', alignItems: 'center', justifyContent: 'center',
                        fontSize: 11, fontWeight: 700, flexShrink: 0,
                      }}>
                        {config.icon}
                      </span>
                      <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text)' }}>
                        {evt.title}
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexShrink: 0 }}>
                      <span style={{ fontSize: 11, color: 'var(--text-subtle)', fontFamily: 'var(--mono)' }}>
                        {formatDate(evt.event_date)}
                      </span>
                      <span style={{ background: config.bg, color: config.color, borderRadius: 99, padding: '1px 7px', fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                        {config.label}
                      </span>
                      {evt.clinical_significance === 'high' && (
                        <span style={{ color: 'var(--danger)', fontSize: 11, fontWeight: 700 }}>★ HIGH</span>
                      )}
                    </div>
                  </div>

                  {/* Expanded view */}
                  {isExpanded && (
                    <div style={{ marginTop: 12, borderTop: '1px solid var(--border)', paddingTop: 12 }}>
                      {evt.description && (
                        <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 10, lineHeight: 1.6 }}>
                          {evt.description}
                        </p>
                      )}
                      {evt.source_document_title && (
                        <SourceBadge title={evt.source_document_title} date={formatDate(evt.event_date)} />
                      )}
                      {evt.evidence.length > 0 && (
                        <div style={{ marginTop: 10 }}>
                          {evt.evidence.map(e => (
                            <div key={e.id} style={{
                              background: 'var(--surface)', border: '1px solid var(--border)',
                              borderRadius: 'var(--radius)', padding: '8px 12px',
                              fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic',
                              lineHeight: 1.6, marginTop: 6,
                            }}>
                              "{e.text}"
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default ClinicalTimeline;
