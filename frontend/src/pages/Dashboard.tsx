import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { seedDemo, getDemoStatus, listPatients, createPatient } from '../services/api';
import type { Patient } from '../types';
import { Card, Button, SectionHeader, Spinner, EmptyState } from '../components/ui';

const Dashboard: React.FC = () => {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [demoLoaded, setDemoLoaded] = useState(false);
  const [seedResult, setSeedResult] = useState<any>(null);
  const [showNewPatient, setShowNewPatient] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ps, status] = await Promise.all([listPatients(), getDemoStatus()]);
      setPatients(ps);
      setDemoLoaded(status.demo_loaded);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSeedDemo = async () => {
    setSeeding(true);
    try {
      const result = await seedDemo();
      setSeedResult(result);
      setDemoLoaded(true);
      await loadData();
    } catch (e) {
      console.error(e);
    } finally {
      setSeeding(false);
    }
  };

  return (
    <div style={{ padding: '32px 40px', maxWidth: 960 }}>
      {/* Header */}
      <div style={{ marginBottom: 36 }}>
        <h1 style={{ fontSize: 28, fontWeight: 800, letterSpacing: '-0.03em', marginBottom: 8 }}>
          THREAD
        </h1>
        <p style={{ fontSize: 15, color: 'var(--text-muted)', maxWidth: 600, lineHeight: 1.6 }}>
          Clinical Continuity Engine — Reconstructs the patient's clinical journey and prevents
          important information from being lost between episodes of care.
        </p>
      </div>

      {/* Architecture diagram */}
      <div style={{
        background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)',
        padding: '20px 24px', marginBottom: 32, display: 'flex', gap: 0, alignItems: 'stretch',
        overflowX: 'auto',
      }}>
        {[
          { label: 'Fragmented Records', sub: 'Upload' },
          { label: 'Clinical Memory', sub: 'Extract & Structure' },
          { label: 'What Changed?', sub: 'Detect' },
          { label: 'Open Loops', sub: 'Identify' },
          { label: 'Conflicts', sub: 'Detect' },
          { label: 'Evidence-Linked Handover', sub: 'Generate' },
        ].map((step, i, arr) => (
          <React.Fragment key={step.label}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', minWidth: 120 }}>
              <div style={{
                background: i === 0 ? 'var(--surface-2)' : i === arr.length - 1 ? 'var(--text)' : 'var(--bg)',
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)', padding: '8px 12px', marginBottom: 6,
                minWidth: 110,
              }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: i === arr.length - 1 ? 'var(--bg)' : 'var(--text)', marginBottom: 2 }}>
                  {step.label}
                </div>
                <div style={{ fontSize: 10, color: i === arr.length - 1 ? 'rgba(255,255,255,0.7)' : 'var(--text-subtle)' }}>
                  {step.sub}
                </div>
              </div>
            </div>
            {i < arr.length - 1 && (
              <div style={{ display: 'flex', alignItems: 'center', padding: '0 4px', color: 'var(--text-subtle)', fontSize: 16 }}>
                →
              </div>
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Demo seeding */}
      {!demoLoaded && (
        <Card style={{ marginBottom: 28, borderLeft: '3px solid var(--accent)', background: 'var(--accent-bg)' }}>
          <SectionHeader title="Load Demo Patient" subtitle="Synthetic demo dataset with realistic clinical complexity" />
          <p style={{ fontSize: 13, color: 'var(--text-muted)', marginBottom: 16, lineHeight: 1.7 }}>
            The demo includes a synthetic patient with 10 documents spanning 9 months, medication changes,
            AKI during admission, a Penicillin allergy conflict, outstanding CT scan, and unresolved nephrology follow-up.
          </p>
          <Button onClick={handleSeedDemo} loading={seeding}>
            Load Demo Patient
          </Button>
        </Card>
      )}

      {seedResult && (
        <div style={{ background: 'var(--success-bg)', border: '1px solid var(--success)', borderRadius: 'var(--radius-lg)', padding: '12px 20px', marginBottom: 24, display: 'flex', gap: 24, alignItems: 'center' }}>
          <span style={{ color: 'var(--success)', fontWeight: 700 }}>✓ Demo loaded</span>
          {Object.entries(seedResult).filter(([k]) => k !== 'status' && k !== 'patient_id').map(([k, v]) => (
            <span key={k} style={{ fontSize: 12, color: 'var(--success)' }}>{v as string} {k}</span>
          ))}
        </div>
      )}

      {/* Patient list */}
      <div style={{ marginBottom: 20, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <SectionHeader title="Patients" count={patients.length} />
        <Button variant="secondary" size="sm" onClick={() => setShowNewPatient(!showNewPatient)}>
          + New Patient
        </Button>
      </div>

      {showNewPatient && <NewPatientForm onCreated={() => { setShowNewPatient(false); loadData(); }} />}

      {loading ? (
        <div style={{ display: 'flex', justifyContent: 'center', padding: 48 }}><Spinner /></div>
      ) : patients.length === 0 ? (
        <EmptyState icon="◎" title="No patients yet" subtitle="Load the demo patient or create a new patient to get started." />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
          {patients.map(p => (
            <PatientRow key={p.id} patient={p} onClick={() => navigate(`/patient/${p.id}`)} />
          ))}
        </div>
      )}
    </div>
  );
};

const PatientRow: React.FC<{ patient: Patient; onClick: () => void }> = ({ patient, onClick }) => (
  <Card onClick={onClick} style={{ cursor: 'pointer' }}>
    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 16 }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
        <div style={{
          width: 40, height: 40, borderRadius: '50%',
          background: 'var(--surface-2)', border: '1px solid var(--border)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 14, fontWeight: 800, color: 'var(--text-muted)',
          flexShrink: 0,
        }}>
          {patient.identifier.slice(0, 2)}
        </div>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{ fontSize: 14, fontWeight: 700, fontFamily: 'var(--mono)' }}>{patient.identifier}</span>
            {patient.age && <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{patient.age}y {patient.sex}</span>}
          </div>
          <div style={{ display: 'flex', gap: 6, marginTop: 4, flexWrap: 'wrap' }}>
            {(patient.major_conditions || []).slice(0, 3).map((c, i) => (
              <span key={i} style={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 99, padding: '1px 8px', fontSize: 11, color: 'var(--text-muted)' }}>{c}</span>
            ))}
            {(patient.major_conditions || []).length > 3 && (
              <span style={{ fontSize: 11, color: 'var(--text-subtle)' }}>+{(patient.major_conditions || []).length - 3} more</span>
            )}
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', gap: 24, flexShrink: 0 }}>
        <Stat label="Documents" value={patient.document_count} />
        <Stat label="Encounters" value={patient.encounter_count} />
        <div style={{ display: 'flex', alignItems: 'center', color: 'var(--text-subtle)', fontSize: 18 }}>›</div>
      </div>
    </div>
  </Card>
);

const Stat: React.FC<{ label: string; value: number }> = ({ label, value }) => (
  <div style={{ textAlign: 'right' }}>
    <div style={{ fontSize: 16, fontWeight: 700 }}>{value}</div>
    <div style={{ fontSize: 10, color: 'var(--text-subtle)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{label}</div>
  </div>
);

const NewPatientForm: React.FC<{ onCreated: () => void }> = ({ onCreated }) => {
  const [identifier, setIdentifier] = useState('');
  const [age, setAge] = useState('');
  const [sex, setSex] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const submit = async () => {
    if (!identifier.trim()) { setError('Identifier required'); return; }
    setLoading(true);
    try {
      await createPatient({ identifier: identifier.trim(), age: age ? parseInt(age) : undefined, sex: sex || undefined, major_conditions: [] });
      onCreated();
    } catch (e: any) {
      setError(e?.response?.data?.detail || 'Failed to create patient');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card style={{ marginBottom: 16 }}>
      <SectionHeader title="New Patient" />
      {error && <div style={{ color: 'var(--danger)', fontSize: 12, marginBottom: 12 }}>{error}</div>}
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        <input value={identifier} onChange={e => setIdentifier(e.target.value)} placeholder="Patient identifier *" style={inputStyle} />
        <input value={age} onChange={e => setAge(e.target.value)} placeholder="Age" type="number" style={{ ...inputStyle, width: 80 }} />
        <select value={sex} onChange={e => setSex(e.target.value)} style={inputStyle}>
          <option value="">Sex</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
        <Button onClick={submit} loading={loading}>Create</Button>
        <Button variant="ghost" onClick={() => {}}>Cancel</Button>
      </div>
    </Card>
  );
};

const inputStyle: React.CSSProperties = {
  border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: '7px 12px',
  fontSize: 13, background: 'var(--bg)', color: 'var(--text)', minWidth: 160,
};

export default Dashboard;
