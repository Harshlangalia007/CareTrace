"""
LLM Service — IBM watsonx.ai abstraction layer.
Keeps the model provider swappable without rewriting application logic.
"""

import json
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """
    Abstract LLM interaction layer.
    In DEMO_MODE, returns structured synthetic responses.
    When watsonx credentials are present, uses IBM watsonx.ai.
    """

    def __init__(self):
        self.demo_mode = settings.demo_mode
        self._client = None

        if not self.demo_mode and settings.watsonx_api_key:
            try:
                from ibm_watsonx_ai.foundation_models import ModelInference
                from ibm_watsonx_ai.credentials import Credentials
                creds = Credentials(
                    url=settings.watsonx_url,
                    api_key=settings.watsonx_api_key
                )
                self._client = ModelInference(
                    model_id=settings.watsonx_model_id,
                    credentials=creds,
                    project_id=settings.watsonx_project_id,
                    params={"max_new_tokens": 1500, "temperature": 0.1}
                )
                logger.info("watsonx.ai client initialised: %s", settings.watsonx_model_id)
            except Exception as e:
                logger.warning("watsonx.ai init failed — falling back to demo mode: %s", e)
                self.demo_mode = True

    def _call(self, prompt: str, max_tokens: int = 1500) -> str:
        if self.demo_mode or self._client is None:
            return self._demo_response(prompt)
        try:
            result = self._client.generate_text(prompt=prompt)
            return result
        except Exception as e:
            logger.error("LLM call failed: %s", e)
            return self._demo_response(prompt)

    def _demo_response(self, prompt: str) -> str:
        """Minimal fallback so the app remains functional without credentials."""
        return "Demo mode: LLM response would appear here with real watsonx.ai credentials."

    # ─────────────────────────────────────────────
    # Task-specific methods
    # ─────────────────────────────────────────────

    def classify_document(self, text: str, filename: str) -> dict:
        """Classify a document by type and extract basic metadata."""
        prompt = f"""You are a clinical document classifier. Analyze the following medical document text.

Document filename: {filename}

Document text (first 2000 chars):
{text[:2000]}

Return a JSON object with:
- "document_type": one of [clinical_note, admission_summary, discharge_summary, lab_result, imaging_report, medication_history, referral_letter, specialist_note, follow_up, other]
- "title": a brief descriptive title
- "document_date": ISO date string if detectable, else null
- "source_author": author/clinician name if present, else null
- "source_institution": institution if present, else null

Return only valid JSON, no explanation."""

        if self.demo_mode:
            return {
                "document_type": "clinical_note",
                "title": f"Clinical Document — {filename}",
                "document_date": None,
                "source_author": None,
                "source_institution": None
            }

        raw = self._call(prompt, max_tokens=300)
        try:
            return json.loads(raw.strip())
        except Exception:
            return {"document_type": "other", "title": filename, "document_date": None,
                    "source_author": None, "source_institution": None}

    def extract_clinical_entities(self, text: str, document_id: str) -> dict:
        """Extract structured clinical entities from document text."""
        prompt = f"""You are a clinical information extraction system. Extract structured clinical entities from the following medical document text.

Text:
{text[:3000]}

Return a JSON object with these arrays (use empty array if none found):
- "conditions": [{{"name": str, "status": "active|resolved|suspected", "onset_date": str|null}}]
- "medications": [{{"name": str, "dose": str|null, "route": str|null, "frequency": str|null, "status": "active|stopped", "stop_reason": str|null}}]
- "investigations": [{{"name": str, "type": str, "date": str|null, "status": "pending|completed"}}]
- "results": [{{"investigation": str, "value": str, "unit": str|null, "interpretation": "normal|high|low|critical|null", "date": str|null}}]
- "events": [{{"type": str, "title": str, "date": str|null, "description": str, "significance": "high|medium|low"}}]
- "open_items": [{{"type": str, "description": str, "evidence_text": str}}]

Return only valid JSON."""

        if self.demo_mode:
            return {
                "conditions": [], "medications": [], "investigations": [],
                "results": [], "events": [], "open_items": []
            }

        raw = self._call(prompt, max_tokens=2000)
        try:
            return json.loads(raw.strip())
        except Exception:
            return {"conditions": [], "medications": [], "investigations": [],
                    "results": [], "events": [], "open_items": []}

    def detect_changes(self, previous_state: str, current_state: str) -> list:
        """Compare clinical states and detect meaningful changes."""
        prompt = f"""You are a clinical change detection system. Compare the previous and current patient state.

PREVIOUS STATE:
{previous_state}

CURRENT STATE:
{current_state}

Identify clinically meaningful changes. Return a JSON array of change objects:
[{{"change_type": str, "title": str, "entity_name": str, "previous_state": str, "current_state": str, "reason": str|null, "evidence_text": str}}]

change_type must be one of: new_diagnosis, worsening, improving, medication_started, medication_stopped, dose_changed, new_investigation, new_result, new_procedure, new_admission, new_referral, treatment_plan_change, allergy_change, follow_up_change, other

Return only valid JSON array."""

        if self.demo_mode:
            return []

        raw = self._call(prompt, max_tokens=1500)
        try:
            return json.loads(raw.strip())
        except Exception:
            return []

    def detect_conflicts(self, document_texts: list) -> list:
        """Detect conflicting information across documents."""
        combined = "\n\n---\n\n".join(
            [f"DOCUMENT {i+1} ({d.get('title','')}, {d.get('date','')}):\n{d.get('text','')[:1000]}"
             for i, d in enumerate(document_texts[:5])]
        )
        prompt = f"""You are a clinical conflict detection system. Identify conflicting information across these documents.

{combined}

Return a JSON array of conflicts:
[{{"title": str, "conflict_type": "allergy|medication|diagnosis|date|dose|other", "severity": "high|medium|low", "source_a_text": str, "source_b_text": str, "description": str, "action_required": str}}]

Return only valid JSON array."""

        if self.demo_mode:
            return []

        raw = self._call(prompt, max_tokens=1500)
        try:
            return json.loads(raw.strip())
        except Exception:
            return []

    def generate_clinician_brief(self, patient_context: str) -> str:
        """Generate the Next Clinician Brief."""
        prompt = f"""You are a clinical documentation assistant. Generate a concise Next Clinician Brief from the following patient context.

PATIENT CONTEXT:
{patient_context[:4000]}

Generate a structured clinical brief with these sections:
1. Why this patient matters
2. What happened (major clinical journey)
3. What changed recently
4. Current state
5. Current medications (evidence-based only)
6. Important previous events
7. Outstanding issues
8. Potential conflicts requiring verification
9. What the next clinician should verify

Use careful clinical language:
- "The record indicates..."
- "The latest available record states..."
- "Potentially outstanding..."
- "No evidence found in the provided records."
- "Conflicting documentation detected."
- "Requires clinician verification."

Clearly mark the output: AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED

Keep it concise and clinically actionable."""

        if self.demo_mode:
            return self._demo_clinician_brief(patient_context)

        return self._call(prompt, max_tokens=2000)

    def generate_ward_round(self, patient_context: str) -> str:
        """Generate a ward round summary."""
        prompt = f"""Generate a concise ward round summary from this patient context.

{patient_context[:3000]}

Include: current status, recent changes, active medications, investigations, outstanding tasks.
Mark as: AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED"""

        if self.demo_mode:
            return self._demo_ward_round(patient_context)

        return self._call(prompt, max_tokens=1500)

    def generate_referral(self, patient_context: str, specialty: str = "") -> str:
        """Generate a referral brief."""
        prompt = f"""Generate an evidence-linked referral brief{' for ' + specialty if specialty else ''} from this patient context.

{patient_context[:3000]}

Include: reason for referral, relevant history, clinical timeline, investigations, treatments, current status, specific question for specialist.
Mark as: AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED"""

        if self.demo_mode:
            return self._demo_referral(patient_context)

        return self._call(prompt, max_tokens=1500)

    def generate_discharge(self, patient_context: str) -> str:
        """Generate a discharge summary draft."""
        prompt = f"""Generate a structured discharge summary draft from this patient context.

{patient_context[:3000]}

Include: admission reason, hospital course, investigations, procedures, medication changes, current status, follow-up requirements, outstanding investigations.
Mark as: AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED"""

        if self.demo_mode:
            return self._demo_discharge(patient_context)

        return self._call(prompt, max_tokens=1500)

    # ─────────────────────────────────────────────
    # Demo fallbacks — realistic structured output
    # ─────────────────────────────────────────────

    def _demo_clinician_brief(self, context: str) -> str:
        return """⚠ AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED

NEXT CLINICIAN BRIEF
If you only have 60 seconds, read this.

WHY THIS PATIENT MATTERS
The record indicates this patient has a complex medical history involving Type 2 Diabetes, Chronic Kidney Disease (Stage 3), and a recent hospital admission for community-acquired pneumonia. Multiple medication changes have been documented across encounters. Potentially outstanding investigations and documentation conflicts require clinician verification.

WHAT HAPPENED
The latest available records indicate: initial GP consultation documented diabetes and early renal impairment; subsequent nephrology referral made; hospital admission for pneumonia with notable renal function deterioration; Metformin stopped during admission due to AKI; discharge with follow-up CT recommended but no CT report found in available records.

WHAT CHANGED RECENTLY
The record indicates Metformin was stopped during the August 2026 admission. Creatinine increased significantly (112 → 287 µmol/L). A CT chest was recommended at discharge. No evidence was found in the provided records confirming the CT occurred.

CURRENT STATE
Most recent record indicates the patient was discharged from City Hospital on 14 August 2026. Current medications include Lisinopril 5mg and Atorvastatin 40mg. Metformin remains stopped. Renal function at discharge: Creatinine 287 µmol/L (high).

CURRENT MEDICATIONS (based on available evidence)
- Lisinopril 5mg OD (active — discharge summary Aug 2026)
- Atorvastatin 40mg ON (active — discharge summary Aug 2026)
- Metformin 500mg BD — STOPPED Aug 2026 (reason: AKI during admission)

OUTSTANDING ISSUES
🔴 Repeat CT chest — requested at discharge, no evidence of completion in available records.
🔴 Nephrology follow-up — referral made Feb 2026, response not documented in available records.
🟡 Renal function monitoring — CKD Stage 3 with recent AKI, repeat U&E not documented post-discharge.

POTENTIAL CONFLICTS
⚠ Allergy documentation conflict: GP record documents Penicillin allergy; August 2026 discharge summary states "No known drug allergies". Requires clinician verification before prescribing.

WHAT THE NEXT CLINICIAN SHOULD VERIFY
1. Confirm whether repeat CT chest occurred — no evidence found in available records.
2. Clarify penicillin allergy status — conflicting documentation detected.
3. Confirm nephrology follow-up status.
4. Review renal function — no post-discharge U&E found in available records.
5. Review diabetes management given Metformin cessation.

SOURCES
- GP Clinical Note — 12 Jan 2026
- Nephrology Referral — 28 Feb 2026
- Admission Clerking — 02 Aug 2026
- Discharge Summary — 14 Aug 2026
- Laboratory Results — Multiple dates"""

    def _demo_ward_round(self, context: str) -> str:
        return """⚠ AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED

WARD ROUND SUMMARY

CURRENT STATUS
Patient admitted 02 Aug 2026 with community-acquired pneumonia. Now Day 12. Clinically improving per nursing notes.

RECENT CHANGES
- CRP trending down (287 → 45 mg/L over 5 days)
- Metformin held — renal function still mildly impaired (Cr 287 µmol/L)
- Switched from IV to oral antibiotics Day 5

ACTIVE MEDICATIONS
- Co-amoxiclav 625mg TDS (Day 5)
- Lisinopril 5mg OD (held during admission — review for restart)
- Atorvastatin 40mg ON

INVESTIGATIONS
- CXR Day 8: Improving right lower lobe consolidation
- U&E Day 10: Cr 287 (↑ from baseline 112), K+ 4.8
- Blood cultures: No growth

OUTSTANDING TASKS
🔴 Renal function remains impaired — U&E recheck needed before discharge
🔴 Decision needed on Lisinopril restart
🟡 Consider nephrology review given CKD + AKI
🟡 Arrange repeat CT chest for 6-week follow-up post-discharge

CONCERNS REQUIRING CLINICIAN REVIEW
- Penicillin allergy conflict — verify before any future penicillin prescribing
- Metformin restart plan pending renal recovery"""

    def _demo_referral(self, context: str) -> str:
        return """⚠ AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED

REFERRAL BRIEF

REASON FOR REFERRAL
Ongoing management of Chronic Kidney Disease Stage 3 with recent acute-on-chronic kidney injury during hospital admission for pneumonia.

RELEVANT HISTORY
The record indicates a background of Type 2 Diabetes (diagnosed Jan 2026) and CKD Stage 3 (baseline Cr 112 µmol/L, eGFR 52 mL/min). Hypertension managed with Lisinopril.

CLINICAL TIMELINE
- Jan 2026: Diabetes and CKD Stage 3 documented at GP
- Feb 2026: Nephrology referral made (response not documented in available records)
- Aug 2026: Hospital admission — CKD complicated by AKI (Cr peak 287 µmol/L)

INVESTIGATIONS
- U&E (Aug 2026): Na 138, K 4.8, Cr 287 µmol/L, Urea 14.2
- eGFR (Aug 2026): 18 mL/min (CKD Stage 4 — acute deterioration)
- Urine PCR: 45 mg/mmol (proteinuria)

TREATMENTS ATTEMPTED
- Lisinopril 5mg OD (held during AKI, restart pending)
- Metformin stopped — AKI (not restarted)
- IV fluids during admission

CURRENT STATUS
Post-discharge. Renal function not yet documented to have returned to baseline.

OUTSTANDING INVESTIGATIONS
- No post-discharge U&E found in available records
- Renal ultrasound not documented

SPECIFIC QUESTION FOR SPECIALIST
The record indicates significant acute deterioration in renal function during recent pneumonia admission. Guidance requested on: (1) safe restart of Lisinopril, (2) diabetes management without Metformin, (3) monitoring plan, (4) CKD progression risk assessment."""

    def _demo_discharge(self, context: str) -> str:
        return """⚠ AI-GENERATED DRAFT — CLINICIAN REVIEW REQUIRED

DISCHARGE SUMMARY DRAFT

ADMISSION REASON
Admitted 02 August 2026 with 5-day history of productive cough, fever (38.9°C), and dyspnoea. CXR confirmed right lower lobe consolidation consistent with community-acquired pneumonia.

HOSPITAL COURSE
The record indicates the patient was treated with IV Co-amoxiclav, transitioned to oral Day 5 following clinical improvement. Renal function deteriorated acutely during admission (Cr 112 → 287 µmol/L — AKI Stage 2).

IMPORTANT INVESTIGATIONS
- CXR admission: RLL consolidation
- CXR Day 8: Improving consolidation
- U&E peak: Cr 287, K 4.8, Urea 14.2
- CRP: 287 mg/L (admission) → 45 mg/L (discharge)
- Blood cultures: No growth

PROCEDURES
- IV cannulation and fluid resuscitation
- Oxygen therapy (Day 1–3)

MEDICATION CHANGES
- Metformin 500mg BD: STOPPED — AKI during admission
- Lisinopril 5mg OD: Held during admission — requires restart decision
- Co-amoxiclav 625mg TDS: Commenced — complete 7-day course

CURRENT STATUS AT DISCHARGE
Clinically improving. Afebrile. Oxygen saturations 97% on air. Renal function mildly impaired at discharge (Cr 287).

FOLLOW-UP REQUIREMENTS
- Repeat U&E in 2 weeks to assess renal recovery
- Repeat CT chest in 6 weeks (to exclude underlying malignancy)
- GP review: Metformin and Lisinopril restart decision
- Nephrology follow-up (outstanding referral — verify status)

OUTSTANDING INVESTIGATIONS
- No post-discharge renal function documented in available records
- Repeat CT chest pending

INFORMATION FOR NEXT CLINICIAN
⚠ Allergy conflict: Penicillin allergy documented in GP records conflicts with "No known drug allergies" in this discharge summary — requires verification."""


# Singleton
llm_service = LLMService()
