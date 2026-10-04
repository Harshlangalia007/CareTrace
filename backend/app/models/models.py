"""
THREAD — SQLAlchemy ORM Models
Relational data model for the Clinical Memory Engine.
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, ForeignKey,
    Float, Integer, JSON, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from app.database import Base
import enum


def gen_id():
    return str(uuid.uuid4())


# ─────────────────────────────────────────────
# Enumerations
# ─────────────────────────────────────────────

class DocumentType(str, enum.Enum):
    CLINICAL_NOTE = "clinical_note"
    ADMISSION_SUMMARY = "admission_summary"
    DISCHARGE_SUMMARY = "discharge_summary"
    LAB_RESULT = "lab_result"
    IMAGING_REPORT = "imaging_report"
    MEDICATION_HISTORY = "medication_history"
    REFERRAL_LETTER = "referral_letter"
    SPECIALIST_NOTE = "specialist_note"
    FOLLOW_UP = "follow_up"
    OTHER = "other"


class EventType(str, enum.Enum):
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    CONSULTATION = "consultation"
    DIAGNOSIS = "diagnosis"
    PROCEDURE = "procedure"
    MEDICATION_START = "medication_start"
    MEDICATION_STOP = "medication_stop"
    MEDICATION_CHANGE = "medication_change"
    INVESTIGATION = "investigation"
    RESULT = "result"
    REFERRAL = "referral"
    FOLLOW_UP = "follow_up"
    ALLERGY = "allergy"
    OTHER = "other"


class LoopStatus(str, enum.Enum):
    OPEN = "open"
    RESOLVED = "resolved"
    UNVERIFIABLE = "unverifiable"


class ConflictSeverity(str, enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ChangeType(str, enum.Enum):
    NEW_DIAGNOSIS = "new_diagnosis"
    WORSENING = "worsening"
    IMPROVING = "improving"
    MEDICATION_STARTED = "medication_started"
    MEDICATION_STOPPED = "medication_stopped"
    DOSE_CHANGED = "dose_changed"
    NEW_INVESTIGATION = "new_investigation"
    NEW_RESULT = "new_result"
    NEW_PROCEDURE = "new_procedure"
    NEW_ADMISSION = "new_admission"
    NEW_REFERRAL = "new_referral"
    TREATMENT_PLAN_CHANGE = "treatment_plan_change"
    ALLERGY_CHANGE = "allergy_change"
    FOLLOW_UP_CHANGE = "follow_up_change"
    OTHER = "other"


class OutputType(str, enum.Enum):
    NEXT_CLINICIAN_BRIEF = "next_clinician_brief"
    WARD_ROUND = "ward_round"
    REFERRAL = "referral"
    DISCHARGE = "discharge"


# ─────────────────────────────────────────────
# Core Models
# ─────────────────────────────────────────────

class Patient(Base):
    __tablename__ = "patients"

    id = Column(String, primary_key=True, default=gen_id)
    identifier = Column(String, unique=True, nullable=False)  # anonymised
    age = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)
    major_conditions = Column(JSON, default=list)  # list of strings
    current_admission = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    documents = relationship("Document", back_populates="patient", cascade="all, delete-orphan")
    encounters = relationship("Encounter", back_populates="patient", cascade="all, delete-orphan")
    clinical_events = relationship("ClinicalEvent", back_populates="patient", cascade="all, delete-orphan")
    conditions = relationship("Condition", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    investigations = relationship("Investigation", back_populates="patient", cascade="all, delete-orphan")
    referrals = relationship("Referral", back_populates="patient", cascade="all, delete-orphan")
    open_loops = relationship("OpenLoop", back_populates="patient", cascade="all, delete-orphan")
    conflicts = relationship("Conflict", back_populates="patient", cascade="all, delete-orphan")
    generated_outputs = relationship("GeneratedOutput", back_populates="patient", cascade="all, delete-orphan")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    filename = Column(String, nullable=False)
    document_type = Column(SAEnum(DocumentType), default=DocumentType.OTHER)
    document_date = Column(DateTime, nullable=True)
    title = Column(String, nullable=True)
    source_author = Column(String, nullable=True)
    source_institution = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    processed = Column(Boolean, default=False)
    file_path = Column(String, nullable=True)
    page_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="documents")
    evidence = relationship("Evidence", back_populates="document")
    clinical_events = relationship("ClinicalEvent", back_populates="source_document")


class Encounter(Base):
    __tablename__ = "encounters"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    encounter_date = Column(DateTime, nullable=False)
    encounter_type = Column(String, nullable=True)  # admission, outpatient, ED, etc.
    location = Column(String, nullable=True)
    clinician = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="encounters")
    clinical_events = relationship("ClinicalEvent", back_populates="encounter")


class ClinicalEvent(Base):
    __tablename__ = "clinical_events"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    encounter_id = Column(String, ForeignKey("encounters.id"), nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    event_type = Column(SAEnum(EventType), nullable=False)
    event_date = Column(DateTime, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    clinical_significance = Column(String, nullable=True)  # high, medium, low
    is_confirmed = Column(Boolean, default=True)
    confidence = Column(Float, default=1.0)  # 0.0–1.0
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="clinical_events")
    encounter = relationship("Encounter", back_populates="clinical_events")
    source_document = relationship("Document", back_populates="clinical_events")
    evidence = relationship("Evidence", back_populates="clinical_event")


class Condition(Base):
    __tablename__ = "conditions"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, default="active")  # active, resolved, suspected
    onset_date = Column(DateTime, nullable=True)
    resolved_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="conditions")


class Medication(Base):
    __tablename__ = "medications"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    name = Column(String, nullable=False)
    dose = Column(String, nullable=True)
    route = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    status = Column(String, default="active")  # active, stopped, on_hold, changed
    start_date = Column(DateTime, nullable=True)
    stop_date = Column(DateTime, nullable=True)
    stop_reason = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="medications")
    changes = relationship("MedicationChange", back_populates="medication", cascade="all, delete-orphan")


class MedicationChange(Base):
    __tablename__ = "medication_changes"

    id = Column(String, primary_key=True, default=gen_id)
    medication_id = Column(String, ForeignKey("medications.id"), nullable=False)
    change_date = Column(DateTime, nullable=False)
    change_type = Column(SAEnum(ChangeType), nullable=False)
    previous_value = Column(String, nullable=True)
    new_value = Column(String, nullable=True)
    reason = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    medication = relationship("Medication", back_populates="changes")


class Investigation(Base):
    __tablename__ = "investigations"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    name = Column(String, nullable=False)
    investigation_type = Column(String, nullable=True)  # blood, imaging, biopsy, etc.
    requested_date = Column(DateTime, nullable=True)
    result_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, completed, cancelled
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="investigations")
    results = relationship("InvestigationResult", back_populates="investigation", cascade="all, delete-orphan")


class InvestigationResult(Base):
    __tablename__ = "investigation_results"

    id = Column(String, primary_key=True, default=gen_id)
    investigation_id = Column(String, ForeignKey("investigations.id"), nullable=False)
    result_date = Column(DateTime, nullable=True)
    value = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    reference_range = Column(String, nullable=True)
    interpretation = Column(String, nullable=True)  # normal, high, low, critical
    notes = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    investigation = relationship("Investigation", back_populates="results")


class Procedure(Base):
    __tablename__ = "procedures"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    name = Column(String, nullable=False)
    procedure_date = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    outcome = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")


class Referral(Base):
    __tablename__ = "referrals"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    specialty = Column(String, nullable=True)
    reason = Column(Text, nullable=True)
    referral_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, responded, cancelled
    response_date = Column(DateTime, nullable=True)
    response_notes = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="referrals")


class FollowUp(Base):
    __tablename__ = "follow_ups"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="pending")  # pending, completed, overdue
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")


class OpenLoop(Base):
    __tablename__ = "open_loops"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    loop_type = Column(String, nullable=True)  # investigation, referral, follow_up, medication_review, etc.
    status = Column(SAEnum(LoopStatus), default=LoopStatus.OPEN)
    requested_date = Column(DateTime, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    evidence_text = Column(Text, nullable=True)
    latest_matching_record = Column(String, nullable=True)
    action_required = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="open_loops")


class Conflict(Base):
    __tablename__ = "conflicts"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    conflict_type = Column(String, nullable=True)  # allergy, medication, diagnosis, date, dose
    severity = Column(SAEnum(ConflictSeverity), default=ConflictSeverity.MEDIUM)
    source_a_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    source_b_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    source_a_text = Column(Text, nullable=True)
    source_b_text = Column(Text, nullable=True)
    action_required = Column(Text, nullable=True)
    resolved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="conflicts")


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=gen_id)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    clinical_event_id = Column(String, ForeignKey("clinical_events.id"), nullable=True)
    extracted_text = Column(Text, nullable=False)
    section = Column(String, nullable=True)
    page_number = Column(Integer, nullable=True)
    confidence = Column(Float, default=1.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    document = relationship("Document", back_populates="evidence")
    clinical_event = relationship("ClinicalEvent", back_populates="evidence")


class DetectedChange(Base):
    __tablename__ = "detected_changes"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    change_type = Column(SAEnum(ChangeType), nullable=False)
    title = Column(String, nullable=False)
    entity_name = Column(String, nullable=True)
    previous_state = Column(Text, nullable=True)
    current_state = Column(Text, nullable=True)
    change_date = Column(DateTime, nullable=True)
    reason = Column(Text, nullable=True)
    source_document_id = Column(String, ForeignKey("documents.id"), nullable=True)
    evidence_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient")


class GeneratedOutput(Base):
    __tablename__ = "generated_outputs"

    id = Column(String, primary_key=True, default=gen_id)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    output_type = Column(SAEnum(OutputType), nullable=False)
    content = Column(Text, nullable=False)
    evidence_refs = Column(JSON, default=list)  # list of document IDs
    generated_at = Column(DateTime, default=datetime.utcnow)
    model_used = Column(String, nullable=True)
    is_demo = Column(Boolean, default=False)

    patient = relationship("Patient", back_populates="generated_outputs")
