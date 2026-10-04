// THREAD — Clinical Continuity Engine
// Shared TypeScript types

export interface Patient {
  id: string;
  identifier: string;
  age?: number;
  sex?: string;
  major_conditions: string[];
  current_admission?: string;
  document_count: number;
  encounter_count: number;
}

export interface Document {
  id: string;
  patient_id: string;
  filename: string;
  document_type: string;
  document_date?: string;
  title?: string;
  source_author?: string;
  source_institution?: string;
  processed: boolean;
}

export type EventType =
  | 'admission' | 'discharge' | 'consultation' | 'diagnosis'
  | 'procedure' | 'medication_start' | 'medication_stop' | 'medication_change'
  | 'investigation' | 'result' | 'referral' | 'follow_up' | 'allergy' | 'other';

export interface TimelineEvent {
  id: string;
  event_type: EventType;
  event_date?: string;
  title: string;
  description?: string;
  clinical_significance?: 'high' | 'medium' | 'low';
  is_confirmed: boolean;
  source_document_id?: string;
  source_document_title?: string;
  evidence: EvidenceItem[];
}

export interface EvidenceItem {
  id: string;
  text: string;
  document_id: string;
}

export interface Condition {
  id: string;
  name: string;
  status: 'active' | 'resolved' | 'suspected';
  onset_date?: string;
  resolved_date?: string;
  notes?: string;
  source_document_id?: string;
}

export interface Medication {
  id: string;
  name: string;
  dose?: string;
  route?: string;
  frequency?: string;
  status: 'active' | 'stopped' | 'on_hold' | 'changed';
  start_date?: string;
  stop_date?: string;
  stop_reason?: string;
  source_document_id?: string;
}

export interface Investigation {
  id: string;
  name: string;
  investigation_type?: string;
  requested_date?: string;
  result_date?: string;
  status: 'pending' | 'completed' | 'cancelled';
  source_document_id?: string;
}

export interface OpenLoop {
  id: string;
  title: string;
  description?: string;
  loop_type?: string;
  status: 'open' | 'resolved' | 'unverifiable';
  requested_date?: string;
  source_document_id?: string;
  evidence_text?: string;
  latest_matching_record?: string;
  action_required?: string;
}

export interface Conflict {
  id: string;
  title: string;
  description?: string;
  conflict_type?: string;
  severity: 'high' | 'medium' | 'low';
  source_a_document_id?: string;
  source_b_document_id?: string;
  source_a_text?: string;
  source_b_text?: string;
  action_required?: string;
  resolved: boolean;
}

export interface DetectedChange {
  id: string;
  change_type: string;
  title: string;
  entity_name?: string;
  previous_state?: string;
  current_state?: string;
  change_date?: string;
  reason?: string;
  source_document_id?: string;
  evidence_text?: string;
}

export interface GeneratedOutput {
  id: string;
  patient_id: string;
  output_type: 'next_clinician_brief' | 'ward_round' | 'referral' | 'discharge';
  content: string;
  evidence_refs: string[];
  generated_at: string;
  model_used?: string;
  is_demo: boolean;
}

export interface ClinicalSummary {
  patient_id: string;
  conditions: { id: string; name: string; status: string }[];
  active_medications: { id: string; name: string; dose?: string; status: string }[];
  stopped_medications: { id: string; name: string; dose?: string; stop_reason?: string }[];
  pending_investigations: { id: string; name: string; status: string }[];
  open_loops_count: number;
  conflicts_count: number;
  recent_changes: { title: string; type: string }[];
  timeline_events: number;
}
