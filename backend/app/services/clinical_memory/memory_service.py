"""
Clinical Memory Service.
Orchestrates the full processing pipeline for a patient's documents.
Produces: ClinicalEvents, Conditions, Medications, Investigations,
          DetectedChanges, OpenLoops, Conflicts.
"""

import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import (
    Document, Patient, Encounter, ClinicalEvent, Condition,
    Medication, MedicationChange, Investigation, OpenLoop,
    Conflict, DetectedChange, Evidence
)
from app.services.llm.llm_service import llm_service

logger = logging.getLogger(__name__)


def process_document(db: Session, document_id: str) -> Document:
    """
    Run the full processing pipeline for a single document.
    """
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc or not doc.raw_text:
        raise ValueError(f"Document {document_id} not found or has no text")

    # Step 1: classify
    meta = llm_service.classify_document(doc.raw_text, doc.filename)
    if meta.get("document_type"):
        doc.document_type = meta["document_type"]
    if meta.get("title"):
        doc.title = meta["title"]
    if meta.get("source_author"):
        doc.source_author = meta["source_author"]
    if meta.get("source_institution"):
        doc.source_institution = meta["source_institution"]
    if meta.get("document_date"):
        try:
            doc.document_date = datetime.fromisoformat(meta["document_date"])
        except Exception:
            pass

    # Step 2: extract entities
    entities = llm_service.extract_clinical_entities(doc.raw_text, doc.id)

    # Persist conditions
    for c in entities.get("conditions", []):
        condition = Condition(
            patient_id=doc.patient_id,
            name=c.get("name", ""),
            status=c.get("status", "active"),
            source_document_id=doc.id,
        )
        if c.get("onset_date"):
            try:
                condition.onset_date = datetime.fromisoformat(c["onset_date"])
            except Exception:
                pass
        db.add(condition)

    # Persist medications
    for m in entities.get("medications", []):
        med = Medication(
            patient_id=doc.patient_id,
            name=m.get("name", ""),
            dose=m.get("dose"),
            route=m.get("route"),
            frequency=m.get("frequency"),
            status=m.get("status", "active"),
            stop_reason=m.get("stop_reason"),
            source_document_id=doc.id,
        )
        db.add(med)

    # Persist investigations
    for inv in entities.get("investigations", []):
        investigation = Investigation(
            patient_id=doc.patient_id,
            name=inv.get("name", ""),
            investigation_type=inv.get("type"),
            status=inv.get("status", "pending"),
            source_document_id=doc.id,
        )
        if inv.get("date"):
            try:
                investigation.requested_date = datetime.fromisoformat(inv["date"])
            except Exception:
                pass
        db.add(investigation)

    # Persist clinical events
    for evt in entities.get("events", []):
        event = ClinicalEvent(
            patient_id=doc.patient_id,
            source_document_id=doc.id,
            event_type=evt.get("type", "other"),
            title=evt.get("title", ""),
            description=evt.get("description", ""),
            clinical_significance=evt.get("significance", "medium"),
        )
        if evt.get("date"):
            try:
                event.event_date = datetime.fromisoformat(evt["date"])
            except Exception:
                pass
        db.add(event)
        db.flush()

        # Create evidence
        ev = Evidence(
            document_id=doc.id,
            clinical_event_id=event.id,
            extracted_text=evt.get("description", "")[:500],
        )
        db.add(ev)

    doc.processed = True
    db.commit()
    db.refresh(doc)
    logger.info("Processed document %s", document_id)
    return doc


def run_change_detection(db: Session, patient_id: str):
    """Detect changes across processed documents for a patient."""
    docs = (
        db.query(Document)
        .filter(Document.patient_id == patient_id, Document.processed == True)
        .order_by(Document.document_date)
        .all()
    )
    if len(docs) < 2:
        return

    doc_texts = [
        {"title": d.title or d.filename, "date": str(d.document_date), "text": d.raw_text or ""}
        for d in docs
    ]

    # Build coarse previous/current state strings
    mid = len(doc_texts) // 2
    previous = "\n\n".join(f"[{d['title']}]\n{d['text'][:500]}" for d in doc_texts[:mid])
    current = "\n\n".join(f"[{d['title']}]\n{d['text'][:500]}" for d in doc_texts[mid:])

    changes = llm_service.detect_changes(previous, current)
    for ch in changes:
        change = DetectedChange(
            patient_id=patient_id,
            change_type=ch.get("change_type", "other"),
            title=ch.get("title", ""),
            entity_name=ch.get("entity_name"),
            previous_state=ch.get("previous_state"),
            current_state=ch.get("current_state"),
            reason=ch.get("reason"),
            evidence_text=ch.get("evidence_text"),
        )
        db.add(change)

    db.commit()
    logger.info("Change detection complete for patient %s", patient_id)


def run_conflict_detection(db: Session, patient_id: str):
    """Detect documentation conflicts for a patient."""
    docs = (
        db.query(Document)
        .filter(Document.patient_id == patient_id, Document.processed == True)
        .order_by(Document.document_date)
        .all()
    )
    doc_texts = [
        {"title": d.title or d.filename, "date": str(d.document_date), "text": d.raw_text or ""}
        for d in docs
    ]

    conflicts = llm_service.detect_conflicts(doc_texts)
    for cf in conflicts:
        conflict = Conflict(
            patient_id=patient_id,
            title=cf.get("title", ""),
            description=cf.get("description", ""),
            conflict_type=cf.get("conflict_type", "other"),
            severity=cf.get("severity", "medium"),
            source_a_text=cf.get("source_a_text"),
            source_b_text=cf.get("source_b_text"),
            action_required=cf.get("action_required"),
        )
        db.add(conflict)

    db.commit()
    logger.info("Conflict detection complete for patient %s", patient_id)


def build_patient_context(db: Session, patient_id: str) -> str:
    """Build a rich patient context string for LLM generation."""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return ""

    from app.models import (Condition, Medication, Investigation,
                            OpenLoop, Conflict, DetectedChange)

    conditions = db.query(Condition).filter(Condition.patient_id == patient_id).all()
    meds = db.query(Medication).filter(Medication.patient_id == patient_id).all()
    docs = (db.query(Document).filter(Document.patient_id == patient_id)
            .order_by(Document.document_date).all())
    open_loops = db.query(OpenLoop).filter(OpenLoop.patient_id == patient_id).all()
    conflicts = db.query(Conflict).filter(Conflict.patient_id == patient_id).all()
    changes = db.query(DetectedChange).filter(DetectedChange.patient_id == patient_id).all()

    lines = [
        f"PATIENT: {patient.identifier} | Age: {patient.age} | Sex: {patient.sex}",
        f"CONDITIONS: {', '.join(c.name for c in conditions)}",
        "",
        "ACTIVE MEDICATIONS:",
    ]
    for m in meds:
        lines.append(f"  - {m.name} {m.dose or ''} {m.frequency or ''} [{m.status}]")

    lines += ["", "RECENT CHANGES:"]
    for ch in changes[:5]:
        lines.append(f"  - {ch.title}: {ch.previous_state} → {ch.current_state}")

    lines += ["", "OPEN LOOPS:"]
    for ol in open_loops:
        lines.append(f"  - {ol.title}: {ol.description or ''}")

    lines += ["", "CONFLICTS:"]
    for cf in conflicts:
        lines.append(f"  - {cf.title}: {cf.description or ''}")

    lines += ["", "DOCUMENTS:"]
    for d in docs:
        lines.append(f"  [{d.document_date}] {d.title or d.filename}")

    return "\n".join(lines)
