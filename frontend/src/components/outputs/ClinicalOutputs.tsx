import React, { useState } from 'react';
import type { GeneratedOutput } from '../../types';
import { Card, Button, Badge, Spinner, Divider } from '../ui';
import {
  generateNextClinicianBrief, generateWardRound,
  generateReferral, generateDischarge
} from '../../services/api';

interface OutputsProps {
  patientId: string;
  onGenerated?: (output: GeneratedOutput) => void;
}

type OutputMode = 'brief' | 'ward_round' | 'referral' | 'discharge' | null;

const ClinicalOutputs: React.FC<OutputsProps> = ({ patientId, onGenerated }) => {
  const [activeMode, setActiveMode] = useState<OutputMode>(null);
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState<GeneratedOutput | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [referralSpecialty, setReferralSpecialty] = useState('');

  const generate = async (mode: OutputMode) => {
    if (!mode) return;
    setLoading(true);
    setError(null);
    setOutput(null);
    setActiveMode(mode);

    try {
      let result: GeneratedOutput;
      if (mode === 'brief') result = await generateNextClinicianBrief(patientId);
      else if (mode === 'ward_round') result = await generateWardRound(patientId);
      else if (mode === 'referral') result = await generateReferral(patientId, referralSpecialty);
      else result = await generateDischarge(patientId);

      setOutput(result);
      onGenerated?.(result);
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Generation failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const modeConfig = {
    brief: {
      title: 'Next Clinician Brief',
      subtitle: 'If you only have 60 seconds, read this.',
      color: 'var(--text)',
      bg: 'var(--surface)',
      icon: '★',
    },
    ward_round: {
      title: 'Ward Round',
      subtitle: 'Current status, changes, medications, outstanding tasks.',
      color: 'var(--accent)',
      bg: 'var(--accent-bg)',
      icon: '♦',
    },
    referral: {
      title: 'Referral',
      subtitle: 'Evidence-linked specialist referral brief.',
      color: 'var(--purple)',
      bg: 'var(--purple-bg)',
      icon: '→',
    },
    discharge: {
      title: 'Discharge',
      subtitle: 'Structured discharge summary draft.',
      color: 'var(--success)',
      bg: 'var(--success-bg)',
      icon: '↗',
    },
  };

  return (
    <div>
      <div style={{ marginBottom: 20 }}>
        <h2 style={{ fontSize: 20, fontWeight: 700, letterSpacing: '-0.02em', marginBottom: 4 }}>Generate Clinical Outputs</h2>
        <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          All generated outputs are AI drafts. Clinician review required before clinical use.
        </p>
      </div>

      {/* Action buttons */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginBottom: 24 }}>
        {(Object.keys(modeConfig) as OutputMode[]).filter(Boolean).map(mode => {
          if (!mode) return null;
          const cfg = modeConfig[mode];
          const isActive = activeMode === mode;
          return (
            <Card
              key={mode}
              onClick={() => generate(mode)}
              style={{
                cursor: 'pointer',
                border: isActive ? `2px solid ${cfg.color}` : '1px solid var(--border)',
                background: isActive ? cfg.bg : 'var(--bg)',
                textAlign: 'center',
                padding: '18px 16px',
              }}
            >
              <div style={{ fontSize: 24, marginBottom: 8 }}>{cfg.icon}</div>
              <div style={{ fontSize: 13, fontWeight: 700, marginBottom: 4, color: isActive ? cfg.color : 'var(--text)' }}>
                {cfg.title}
              </div>
              <div style={{ fontSize: 11, color: 'var(--text-subtle)', lineHeight: 1.4 }}>{cfg.subtitle}</div>

              {mode === 'referral' && isActive && !loading && (
                <input
                  value={referralSpecialty}
                  onChange={e => setReferralSpecialty(e.target.value)}
                  placeholder="Specialty (optional)"
                  onClick={e => e.stopPropagation()}
                  style={{
                    marginTop: 10, width: '100%',
                    border: '1px solid var(--border)', borderRadius: 'var(--radius)',
                    padding: '5px 8px', fontSize: 12, background: 'var(--bg)',
                  }}
                />
              )}
            </Card>
          );
        })}
      </div>

      {loading && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 20, color: 'var(--text-muted)' }}>
          <Spinner />
          <span>Generating {activeMode ? modeConfig[activeMode]?.title : 'output'}…</span>
        </div>
      )}

      {error && (
        <div style={{ background: 'var(--danger-bg)', border: '1px solid var(--danger)', borderRadius: 'var(--radius)', padding: 14, color: 'var(--danger)', marginBottom: 16 }}>
          {error}
        </div>
      )}

      {output && (
        <Card>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 16 }}>
            <div>
              <h3 style={{ fontSize: 16, fontWeight: 700, marginBottom: 4 }}>
                {activeMode ? modeConfig[activeMode]?.title : 'Output'}
              </h3>
              <Badge variant="warning">AI-Generated Draft — Clinician Review Required</Badge>
            </div>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => {
                const blob = new Blob([output.content], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${activeMode}_${patientId}.txt`;
                a.click();
              }}
            >
              Export
            </Button>
          </div>

          <Divider />

          {/* Render output as formatted text */}
          <div style={{ fontFamily: 'var(--mono)', fontSize: 13, lineHeight: 1.8, whiteSpace: 'pre-wrap', color: 'var(--text)' }}>
            {output.content.split('\n').map((line, i) => {
              // Style section headers
              if (line.match(/^[A-Z][A-Z ]+$/) && line.trim().length > 2) {
                return (
                  <div key={i} style={{ fontFamily: 'var(--font)', fontWeight: 800, fontSize: 12, letterSpacing: '0.08em', color: 'var(--text)', borderTop: i > 0 ? '1px solid var(--border)' : 'none', paddingTop: i > 0 ? 12 : 0, marginTop: i > 0 ? 12 : 0, marginBottom: 4 }}>
                    {line}
                  </div>
                );
              }
              if (line.startsWith('⚠') || line.startsWith('🔴') || line.startsWith('🟡') || line.startsWith('🟢')) {
                return (
                  <div key={i} style={{ padding: '4px 0', lineHeight: 1.6, fontFamily: 'var(--font)', fontSize: 13 }}>
                    {line}
                  </div>
                );
              }
              if (line.startsWith('# ') || line.startsWith('## ')) {
                return (
                  <div key={i} style={{ fontFamily: 'var(--font)', fontWeight: 700, fontSize: line.startsWith('# ') ? 18 : 15, color: 'var(--text)', marginTop: 16, marginBottom: 6, letterSpacing: '-0.01em' }}>
                    {line.replace(/^#+\s*/, '')}
                  </div>
                );
              }
              if (line.startsWith('- ') || line.startsWith('• ')) {
                return (
                  <div key={i} style={{ paddingLeft: 16, lineHeight: 1.7, fontFamily: 'var(--font)', fontSize: 13 }}>
                    {line}
                  </div>
                );
              }
              return (
                <div key={i} style={{ lineHeight: 1.7, fontFamily: 'var(--font)', fontSize: 13 }}>
                  {line}
                </div>
              );
            })}
          </div>
        </Card>
      )}
    </div>
  );
};

export default ClinicalOutputs;
