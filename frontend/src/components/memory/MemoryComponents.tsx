import React, { useState } from 'react';
import { format, parseISO } from 'date-fns';
import type { OpenLoop, Conflict, DetectedChange } from '../../types';
import { Card, Badge, SourceBadge, EmptyState } from '../ui';

// ─────────────────────────────────────────────────────────────────────────────
// What Changed?
// ─────────────────────────────────────────────────────────────────────────────

interface WhatChangedProps {
  changes: DetectedChange[];
  getDocumentTitle?: (id: string) => string;
}

function formatDate(dateStr?: string) {
  if (!dateStr) return '';
  try { return format(parseISO(dateStr), 'dd MMM yyyy'); } catch { return ''; }
}

const changeTypeConfig: Record<string, { label: string; variant: 'danger' | 'warning' | 'success' | 'accent' | 'purple' | 'default' }> = {
  medication_stopped: { label: 'Medication Stopped', variant: 'danger' },
  medication_started: { label: 'Medication Started', variant: 'success' },
  dose_changed: { label: 'Dose Changed', variant: 'warning' },
  new_diagnosis: { label: 'New Diagnosis', variant: 'purple' },
  worsening: { label: 'Worsening', variant: 'danger' },
  improving: { label: 'Improving', variant: 'success' },
  new_admission: { label: 'New Admission', variant: 'danger' },
  new_referral: { label: 'New Referral', variant: 'accent' },
  new_result: { label: 'New Result', variant: 'default' },
  treatment_plan_change: { label: 'Treatment Plan Change', variant: 'warning' },
  allergy_change: { label: 'Allergy Change', variant: 'danger' },
  other: { label: 'Change', variant: 'default' },
};

export const WhatChanged: React.FC<WhatChangedProps> = ({ changes, getDocumentTitle }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (changes.length === 0) {
    return <EmptyState icon="⟳" title="No changes detected" subtitle="Process patient documents to detect clinical changes." />;
  }

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700, letterSpacing: '-0.02em', marginBottom: 4 }}>What Changed?</h2>
        <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          Detected changes comparing across all patient records. The record indicates the following changes.
        </p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
        {changes.map(ch => {
          const config = changeTypeConfig[ch.change_type] || changeTypeConfig.other;
          const isExpanded = expandedId === ch.id;
          return (
            <Card key={ch.id}
              onClick={() => setExpandedId(isExpanded ? null : ch.id)}
              style={{ cursor: 'pointer', borderLeft: `3px solid ${getVariantColor(config.variant)}` }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 16 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <Badge variant={config.variant}>{config.label}</Badge>
                    {ch.entity_name && <span style={{ fontSize: 14, fontWeight: 700 }}>{ch.entity_name}</span>}
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: '1fr auto 1fr', gap: 12, alignItems: 'center' }}>
                    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: '8px 12px' }}>
                      <div style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-subtle)', marginBottom: 4 }}>Previously</div>
                      <div style={{ fontSize: 13, color: 'var(--text-muted)' }}>{ch.previous_state || 'Not documented'}</div>
                    </div>
                    <div style={{ fontSize: 18, color: 'var(--text-subtle)' }}>→</div>
                    <div style={{ background: 'var(--surface)', border: `1px solid ${getVariantColor(config.variant)}`, borderRadius: 'var(--radius)', padding: '8px 12px' }}>
                      <div style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-subtle)', marginBottom: 4 }}>Latest</div>
                      <div style={{ fontSize: 13, fontWeight: 600, color: 'var(--text)' }}>{ch.current_state || 'Not documented'}</div>
                    </div>
                  </div>
                </div>

                <div style={{ textAlign: 'right', flexShrink: 0 }}>
                  <div style={{ fontSize: 11, color: 'var(--text-subtle)', fontFamily: 'var(--mono)' }}>{formatDate(ch.change_date)}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-subtle)', marginTop: 4 }}>{isExpanded ? '▲ Less' : '▼ Evidence'}</div>
                </div>
              </div>

              {isExpanded && (
                <div style={{ marginTop: 12, borderTop: '1px solid var(--border)', paddingTop: 12 }}>
                  {ch.reason && (
                    <div style={{ marginBottom: 10 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-subtle)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Reason: </span>
                      <span style={{ fontSize: 13 }}>{ch.reason}</span>
                    </div>
                  )}
                  {ch.evidence_text && (
                    <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: '10px 14px', fontSize: 13, color: 'var(--text-muted)', fontStyle: 'italic', lineHeight: 1.6, marginBottom: 10 }}>
                      "{ch.evidence_text}"
                    </div>
                  )}
                  {ch.source_document_id && (
                    <SourceBadge title={getDocumentTitle?.(ch.source_document_id) || 'Source Document'} date={formatDate(ch.change_date)} />
                  )}
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Open Loops
// ─────────────────────────────────────────────────────────────────────────────

interface OpenLoopsProps {
  loops: OpenLoop[];
  getDocumentTitle?: (id: string) => string;
}

export const OpenLoops: React.FC<OpenLoopsProps> = ({ loops, getDocumentTitle }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const openLoops = loops.filter(l => l.status === 'open');

  if (openLoops.length === 0) {
    return <EmptyState icon="○" title="No open loops detected" subtitle="All documented follow-ups appear to be accounted for in the available records." />;
  }

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700, letterSpacing: '-0.02em', marginBottom: 4 }}>Open Loops</h2>
        <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          Clinically relevant tasks, investigations, referrals, or follow-ups that appear not to have been completed
          in the available records. Use careful clinical judgment — absence from records does not confirm non-occurrence.
        </p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        {openLoops.map(loop => {
          const isExpanded = expandedId === loop.id;
          return (
            <Card
              key={loop.id}
              onClick={() => setExpandedId(isExpanded ? null : loop.id)}
              style={{ cursor: 'pointer', borderLeft: '3px solid var(--danger)' }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 12 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                    <span style={{ fontSize: 16, color: 'var(--danger)' }}>●</span>
                    <span style={{ fontSize: 14, fontWeight: 700 }}>{loop.title}</span>
                    <Badge variant="danger">Potentially Outstanding</Badge>
                    {loop.loop_type && <Badge variant="default">{loop.loop_type}</Badge>}
                  </div>
                  {loop.description && (
                    <p style={{ fontSize: 13, color: 'var(--text-muted)', lineHeight: 1.6, marginLeft: 24 }}>
                      {loop.description}
                    </p>
                  )}
                </div>
                <div style={{ textAlign: 'right', flexShrink: 0 }}>
                  {loop.requested_date && <div style={{ fontSize: 11, color: 'var(--text-subtle)', fontFamily: 'var(--mono)' }}>Requested: {formatDate(loop.requested_date)}</div>}
                  <div style={{ fontSize: 11, color: 'var(--text-subtle)', marginTop: 4 }}>{isExpanded ? '▲' : '▼ Details'}</div>
                </div>
              </div>

              {isExpanded && (
                <div style={{ marginTop: 12, borderTop: '1px solid var(--border)', paddingTop: 12, marginLeft: 24 }}>
                  {loop.evidence_text && (
                    <div style={{ marginBottom: 12 }}>
                      <div style={{ fontSize: 11, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-subtle)', marginBottom: 6 }}>Evidence</div>
                      <div style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: '10px 14px', fontSize: 13, color: 'var(--text-muted)', fontStyle: 'italic', lineHeight: 1.6 }}>
                        "{loop.evidence_text}"
                      </div>
                    </div>
                  )}
                  {loop.latest_matching_record && (
                    <div style={{ marginBottom: 10 }}>
                      <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-subtle)', textTransform: 'uppercase', letterSpacing: '0.06em' }}>Latest matching record: </span>
                      <span style={{ fontSize: 13, color: 'var(--text-muted)', fontStyle: 'italic' }}>{loop.latest_matching_record}</span>
                    </div>
                  )}
                  {loop.action_required && (
                    <div style={{ background: 'var(--warning-bg)', border: '1px solid var(--warning)', borderRadius: 'var(--radius)', padding: '10px 14px', marginBottom: 10 }}>
                      <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--warning)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 4 }}>Action Required</div>
                      <div style={{ fontSize: 13, color: 'var(--text)' }}>{loop.action_required}</div>
                    </div>
                  )}
                  {loop.source_document_id && (
                    <SourceBadge title={getDocumentTitle?.(loop.source_document_id) || 'Source Document'} date={formatDate(loop.requested_date)} />
                  )}
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Conflicts
// ─────────────────────────────────────────────────────────────────────────────

interface ConflictsProps {
  conflicts: Conflict[];
  getDocumentTitle?: (id: string) => string;
}

export const Conflicts: React.FC<ConflictsProps> = ({ conflicts, getDocumentTitle }) => {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const activeConflicts = conflicts.filter(c => !c.resolved);

  if (activeConflicts.length === 0) {
    return <EmptyState icon="⚡" title="No conflicts detected" subtitle="No contradictory documentation was found across the available records." />;
  }

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700, letterSpacing: '-0.02em', marginBottom: 4 }}>Documentation Conflicts</h2>
        <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          Conflicting information detected across patient records. These require clinician verification.
          THREAD does not determine which record is correct.
        </p>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        {activeConflicts.map(cf => {
          const isExpanded = expandedId === cf.id;
          const borderColor = cf.severity === 'high' ? 'var(--danger)' : cf.severity === 'medium' ? 'var(--warning)' : 'var(--border-strong)';
          return (
            <Card
              key={cf.id}
              onClick={() => setExpandedId(isExpanded ? null : cf.id)}
              style={{ cursor: 'pointer', borderLeft: `3px solid ${borderColor}` }}
            >
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 12 }}>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
                    <span style={{ fontSize: 15, color: cf.severity === 'high' ? 'var(--danger)' : 'var(--warning)' }}>⚡</span>
                    <span style={{ fontSize: 14, fontWeight: 700 }}>{cf.title}</span>
                    <Badge variant={cf.severity === 'high' ? 'danger' : 'warning'}>
                      {cf.severity.toUpperCase()} SEVERITY
                    </Badge>
                    <Badge variant="default">⚠ Conflicting Documentation</Badge>
                  </div>
                  {cf.description && (
                    <p style={{ fontSize: 13, color: 'var(--text-muted)', lineHeight: 1.6, marginLeft: 24 }}>
                      {cf.description.slice(0, 180)}{cf.description.length > 180 ? '…' : ''}
                    </p>
                  )}
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-subtle)', flexShrink: 0 }}>{isExpanded ? '▲' : '▼ Details'}</div>
              </div>

              {isExpanded && (
                <div style={{ marginTop: 14, borderTop: '1px solid var(--border)', paddingTop: 14 }}>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12, marginBottom: 14 }}>
                    <ConflictSource
                      label="Earlier Record"
                      text={cf.source_a_text}
                      docTitle={cf.source_a_document_id ? (getDocumentTitle?.(cf.source_a_document_id) || 'Document A') : undefined}
                    />
                    <ConflictSource
                      label="Later Record"
                      text={cf.source_b_text}
                      docTitle={cf.source_b_document_id ? (getDocumentTitle?.(cf.source_b_document_id) || 'Document B') : undefined}
                      highlight
                    />
                  </div>

                  {cf.action_required && (
                    <div style={{ background: 'var(--warning-bg)', border: '1px solid var(--warning)', borderRadius: 'var(--radius)', padding: '10px 14px' }}>
                      <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--warning)', textTransform: 'uppercase', letterSpacing: '0.06em', marginBottom: 4 }}>Action Required</div>
                      <div style={{ fontSize: 13, color: 'var(--text)' }}>{cf.action_required}</div>
                    </div>
                  )}
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
};

const ConflictSource: React.FC<{ label: string; text?: string; docTitle?: string; highlight?: boolean }> = ({
  label, text, docTitle, highlight
}) => (
  <div style={{
    background: highlight ? 'var(--warning-bg)' : 'var(--surface)',
    border: `1px solid ${highlight ? 'var(--warning)' : 'var(--border)'}`,
    borderRadius: 'var(--radius)',
    padding: '10px 14px',
  }}>
    <div style={{ fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--text-subtle)', marginBottom: 6 }}>
      {label}
    </div>
    {text && <p style={{ fontSize: 13, color: 'var(--text)', lineHeight: 1.6, fontStyle: 'italic', marginBottom: 8 }}>"{text}"</p>}
    {docTitle && <SourceBadge title={docTitle} />}
  </div>
);

function getVariantColor(variant: string): string {
  const map: Record<string, string> = {
    danger: 'var(--danger)', warning: 'var(--warning)', success: 'var(--success)',
    accent: 'var(--accent)', purple: 'var(--purple)', default: 'var(--border)',
  };
  return map[variant] || 'var(--border)';
}
