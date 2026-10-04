import axios from 'axios';
import type {
  Patient, Document, TimelineEvent, Condition, Medication,
  Investigation, OpenLoop, Conflict, DetectedChange,
  GeneratedOutput, ClinicalSummary
} from '../types';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({ baseURL: BASE_URL });

// ─── Demo ───────────────────────────────────────────────────────────────────

export const seedDemo = () => api.post('/demo/seed').then(r => r.data);
export const getDemoStatus = () => api.get('/demo/status').then(r => r.data);

// ─── Patients ────────────────────────────────────────────────────────────────

export const listPatients = (): Promise<Patient[]> =>
  api.get('/patients/').then(r => r.data);

export const getPatient = (id: string): Promise<Patient> =>
  api.get(`/patients/${id}`).then(r => r.data);

export const createPatient = (data: Partial<Patient>): Promise<Patient> =>
  api.post('/patients/', data).then(r => r.data);

// ─── Documents ───────────────────────────────────────────────────────────────

export const listDocuments = (patientId: string): Promise<Document[]> =>
  api.get(`/documents/patient/${patientId}`).then(r => r.data);

export const getDocumentText = (docId: string): Promise<{ id: string; title: string; raw_text: string }> =>
  api.get(`/documents/${docId}/text`).then(r => r.data);

export const uploadDocument = (patientId: string, file: File, documentType?: string): Promise<Document> => {
  const form = new FormData();
  form.append('file', file);
  if (documentType) form.append('document_type', documentType);
  return api.post(`/documents/upload/${patientId}`, form).then(r => r.data);
};

// ─── Clinical Memory ─────────────────────────────────────────────────────────

export const getClinicalSummary = (patientId: string): Promise<ClinicalSummary> =>
  api.get(`/memory/${patientId}/summary`).then(r => r.data);

export const getConditions = (patientId: string): Promise<Condition[]> =>
  api.get(`/memory/${patientId}/conditions`).then(r => r.data);

export const getMedications = (patientId: string): Promise<Medication[]> =>
  api.get(`/memory/${patientId}/medications`).then(r => r.data);

export const getInvestigations = (patientId: string): Promise<Investigation[]> =>
  api.get(`/memory/${patientId}/investigations`).then(r => r.data);

export const getOpenLoops = (patientId: string): Promise<OpenLoop[]> =>
  api.get(`/memory/${patientId}/open-loops`).then(r => r.data);

export const getConflicts = (patientId: string): Promise<Conflict[]> =>
  api.get(`/memory/${patientId}/conflicts`).then(r => r.data);

export const getChanges = (patientId: string): Promise<DetectedChange[]> =>
  api.get(`/memory/${patientId}/changes`).then(r => r.data);

// ─── Timeline ────────────────────────────────────────────────────────────────

export const getTimeline = (patientId: string): Promise<TimelineEvent[]> =>
  api.get(`/timeline/${patientId}`).then(r => r.data);

// ─── Outputs ─────────────────────────────────────────────────────────────────

export const generateNextClinicianBrief = (patientId: string): Promise<GeneratedOutput> =>
  api.post(`/outputs/${patientId}/next-clinician-brief`).then(r => r.data);

export const generateWardRound = (patientId: string): Promise<GeneratedOutput> =>
  api.post(`/outputs/${patientId}/ward-round`).then(r => r.data);

export const generateReferral = (patientId: string, specialty?: string): Promise<GeneratedOutput> =>
  api.post(`/outputs/${patientId}/referral`, { specialty }).then(r => r.data);

export const generateDischarge = (patientId: string): Promise<GeneratedOutput> =>
  api.post(`/outputs/${patientId}/discharge`).then(r => r.data);

export const getOutputHistory = (patientId: string): Promise<GeneratedOutput[]> =>
  api.get(`/outputs/${patientId}/history`).then(r => r.data);

export const getLatestOutput = (patientId: string, outputType: string): Promise<GeneratedOutput> =>
  api.get(`/outputs/${patientId}/latest/${outputType}`).then(r => r.data);
