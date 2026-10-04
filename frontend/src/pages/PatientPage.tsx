import React, { useEffect, useState, useCallback } from 'react';
import { useParams, useNavigate, Routes, Route, Navigate } from 'react-router-dom';
import {
  getPatient, getClinicalSummary, getConditions, getMedications,
  getInvestigations, getOpenLoops, getConflicts, getChanges,
  getTimeline, listDocuments, uploadDocument
} from '../services/api';
import type {
  Patient, ClinicalSummary, Condition, Medication, Investigation,
  OpenLoop, Conflict, DetectedChange, TimelineEvent, Document
} from '../types';
import PatientHeader from '../components/dashboard/PatientHeader';
import ClinicalSnapshot from '../components/dashboard/ClinicalSnapshot';
import ClinicalTimeline from '../components/timeline/ClinicalTimeline';
import { WhatChanged, OpenLoops, Conflicts } from '../components/memory/MemoryComponents';
import ClinicalOutputs from '../components/outputs/ClinicalOutputs';
import { Card, SectionHeader, Button, Spinner, EmptyState, Divider } from '../components/ui';

interface PatientPageData {
  patient: Patient | null;
  summary: ClinicalSummary | null;
  conditions: Condition[];
  medications: Medication[];
  investigations: Investigation[];
  openLoops: OpenLoop[];
  conflicts: Conflict[];
  changes: DetectedChange[];
  timeline: TimelineEvent[];
  documents: Document[];
}

const PatientPage: React.FC = () => {
  const { patientId } = useParams<{ patientId: string }>();
  const navigate = useNavigate();
  const [data, setData] = useState<PatientPageData>({
    patient: null, summary: null, conditions: [], medications: [],
    investigations: [], openLoops: [], conflicts: [], changes: [],
    timeline: [], documents: [],
  });
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!patientId) return;
    setLoading(true);
    try {
      const [patient, summary, conditions, medications, investigations,
        openLoops, conflicts, changes, timeline, documents] = await Promise.all([
        getPatient(patientId),
        getClinicalSummary(patientId),
        getConditions(patientId),
        getMedications(patientId),
        getInvestigations(patientId),
        getOpenLoops(patientId),
        getConflicts(patientId),
        getChanges(patientId),
        getTimeline(patientId),
        listDocuments(patientId),
      ]);
      setData({ patient, summary, conditions, medications, investigations, openLoops, conflicts, changes, timeline, documents });
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, [patientId]);

  useEffect(() => { load(); }, [load]);

  const getDocumentTitle = useCallback((id: string): string => {
    const doc = data.documents.find(d => d.id === id);
    return doc?.title || doc?.filename || id;
  }, [data.documents]);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <Spinner />
      </div>
    );
  }

  if (!data.patient) {
    return <div style={{ padding: 40 }}>Patient not found.</div>;
  }

  const { patient, summary, conditions, medications, openLoops, conflicts, changes, timeline, documents } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <PatientHeader patient={patient} summary={summary || undefined} />

      <div style={{ flex: 1, overflow: 'auto' }}>
        <Routes>
          {/* Overview */}
          <Route path="/" element={
            <div style={{ padding: '24px 28px' }}>
              <ClinicalSnapshot
                summary={summary!}
                openLoops={openLoops}
                conflicts={conflicts}
                changes={changes}
                conditions={conditions}
                medications={medications}
                onViewLoops={() => navigate(`/patient/${patientId}/loops`)}
                onViewConflicts={() => navigate(`/patient/${patientId}/conflicts`)}
                onViewChanges={() => navigate(`/patient/${patientId}/changes`)}
              />
            </div>
          } />

          {/* Timeline */}
          <Route path="/timeline" element={
            <div style={{ padding: '24px 28px' }}>
              <div style={{ marginBottom: 20 }}>
                <h2 style={{ fontSize: 20, fontWeight: 700, letterSpacing: '-0.02em', marginBottom: 4 }}>Clinical Timeline</h2>
                <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
                  Chronological reconstruction of clinical events from all available records.
                  Click any event to view details and evidence.
                </p>
              </div>
              <ClinicalTimeline events={timeline} />
            </div>
          } />

          {/* What Changed */}
          <Route path="/changes" element={
            <div style={{ padding: '24px 28px' }}>
              <WhatChanged changes={changes} getDocumentTitle={getDocumentTitle} />
            </div>
          } />

          {/* Open Loops */}
          <Route path="/loops" element={
            <div style={{ padding: '24px 28px' }}>
              <OpenLoops loops={openLoops} getDocumentTitle={getDocumentTitle} />
            </div>
          } />

          {/* Conflicts */}
          <Route path="/conflicts" element={
            <div style={{ padding: '24px 28px' }}>
              <Conflicts conflicts={conflicts} getDocumentTitle={getDocumentTitle} />
            </div>
          } />

          {/* Evidence / Documents */}
          <Route path="/evidence" element={
            <div style={{ padding: '24px 28px' }}>
              <EvidenceView documents={documents} patientId={patientId!} onRefresh={load} />
            </div>
          } />

          <Route path="/documents" element={
            <div style={{ padding: '24px 28px' }}>
              <EvidenceView documents={documents} patientId={patientId!} onRefresh={load} />
            </div>
          } />

          {/* Outputs */}
          <Route path="/brief" element={
            <div style={{ padding: '24px 28px' }}>
              <ClinicalOutputs patientId={patientId!} />
            </div>
          } />
          <Route path="/ward-round" element={
            <div style={{ padding: '24px 28px' }}>
              <ClinicalOutputs patientId={patientId!} />
            </div>
          } />
          <Route path="/referral" element={
            <div style={{ padding: '24px 28px' }}>
              <ClinicalOutputs patientId={patientId!} />
            </div>
          } />
          <Route path="/discharge" element={
            <div style={{ padding: '24px 28px' }}>
              <ClinicalOutputs patientId={patientId!} />
            </div>
          } />

          <Route path="*" element={<Navigate to={`/patient/${patientId}`} replace />} />
        </Routes>
      </div>
    </div>
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// Evidence / Documents view
// ─────────────────────────────────────────────────────────────────────────────

const docTypeLabels: Record<string, string> = {
  clinical_note: 'Clinical Note',
  admission_summary: 'Admission Summary',
  discharge_summary: 'Discharge Summary',
  lab_result: 'Lab Result',
  imaging_report: 'Imaging Report',
  medication_history: 'Medication History',
  referral_letter: 'Referral Letter',
  specialist_note: 'Specialist Note',
  follow_up: 'Follow-up',
  other: 'Other',
};

import { format, parseISO } from 'date-fns';
import { getDocumentText } from '../services/api';

const EvidenceView: React.FC<{ documents: Document[]; patientId: string; onRefresh: () => void }> = ({
  documents, patientId, onRefresh
}) => {
  const [selectedDoc, setSelectedDoc] = useState<Document | null>(null);
  const [docText, setDocText] = useState<string | null>(null);
  const [loadingText, setLoadingText] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [showUpload, setShowUpload] = useState(false);

  const loadDocText = async (doc: Document) => {
    setSelectedDoc(doc);
    setDocText(null);
    setLoadingText(true);
    try {
      const result = await getDocumentText(doc.id);
      setDocText(result.raw_text);
    } catch (e) {
      setDocText('Failed to load document text.');
    } finally {
      setLoadingText(false);
    }
  };

  const handleUpload = async (file: File) => {
    setUploading(true);
    try {
      await uploadDocument(patientId, file);
      onRefresh();
      setShowUpload(false);
    } catch (e) {
      console.error(e);
    } finally {
      setUploading(false);
    }
  };

  function formatDate(dateStr?: string) {
    if (!dateStr) return '';
    try { return format(parseISO(dateStr), 'dd MMM yyyy'); } catch { return ''; }
  }

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 20 }}>
        <div>
          <h2 style={{ fontSize: 20, fontWeight: 700, letterSpacing: '-0.02em', marginBottom: 4 }}>Source Documents</h2>
          <p style={{ fontSize: 13, color: 'var(--text-muted)' }}>
            All uploaded records. Click a document to view its full text and evidence.
          </p>
        </div>
        <Button variant="secondary" size="sm" onClick={() => setShowUpload(!showUpload)}>
          Upload Document
        </Button>
      </div>

      {showUpload && (
        <Card style={{ marginBottom: 20, background: 'var(--surface)' }}>
          <SectionHeader title="Upload Document" />
          <input
            type="file"
            accept=".txt,.pdf,.docx"
            onChange={e => { const f = e.target.files?.[0]; if (f) handleUpload(f); }}
            style={{ fontSize: 13 }}
          />
          {uploading && <div style={{ marginTop: 10, display: 'flex', gap: 8, alignItems: 'center', color: 'var(--text-muted)', fontSize: 13 }}><Spinner /> Uploading and processing…</div>}
        </Card>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '300px 1fr', gap: 16, height: 600 }}>
        {/* Document list */}
        <div style={{ border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', overflow: 'auto' }}>
          {documents.length === 0 ? (
            <EmptyState icon="◻" title="No documents" subtitle="Upload records to begin." />
          ) : (
            documents.map((doc, i) => (
              <div
                key={doc.id}
                onClick={() => loadDocText(doc)}
                style={{
                  padding: '12px 16px',
                  borderBottom: i < documents.length - 1 ? '1px solid var(--border)' : 'none',
                  cursor: 'pointer',
                  background: selectedDoc?.id === doc.id ? 'var(--accent-bg)' : 'transparent',
                  borderLeft: selectedDoc?.id === doc.id ? '2px solid var(--accent)' : '2px solid transparent',
                }}
              >
                <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 2 }}>{doc.title || doc.filename}</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 4 }}>
                  <span style={{ fontSize: 10, background: 'var(--surface-2)', borderRadius: 99, padding: '1px 6px', color: 'var(--text-muted)' }}>
                    {docTypeLabels[doc.document_type] || doc.document_type}
                  </span>
                  {doc.document_date && (
                    <span style={{ fontSize: 10, color: 'var(--text-subtle)', fontFamily: 'var(--mono)' }}>
                      {formatDate(doc.document_date)}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Document text */}
        <div style={{ border: '1px solid var(--border)', borderRadius: 'var(--radius-lg)', overflow: 'auto', padding: 20 }}>
          {!selectedDoc ? (
            <EmptyState icon="◈" title="Select a document" subtitle="Click any document to view its full content." />
          ) : loadingText ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: 40 }}><Spinner /></div>
          ) : (
            <div>
              <div style={{ marginBottom: 16 }}>
                <h3 style={{ fontSize: 15, fontWeight: 700, marginBottom: 4 }}>{selectedDoc.title || selectedDoc.filename}</h3>
                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                  {selectedDoc.source_author && <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{selectedDoc.source_author}</span>}
                  {selectedDoc.source_institution && <span style={{ fontSize: 11, color: 'var(--text-subtle)' }}>· {selectedDoc.source_institution}</span>}
                </div>
              </div>
              <Divider />
              <pre style={{
                fontFamily: 'var(--mono)', fontSize: 12, lineHeight: 1.8, color: 'var(--text)',
                whiteSpace: 'pre-wrap', wordBreak: 'break-word',
              }}>
                {docText || 'No text content available.'}
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PatientPage;
