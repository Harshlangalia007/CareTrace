"""
Synthetic demo dataset for THREAD.
Creates a realistic patient with fragmented records across multiple encounters.
Deliberately includes:
- 2+ documentation conflicts
- 3+ open loops
- Medication change with evidence
- Investigation requested but no result found
"""

import uuid
from datetime import datetime, timezone

DEMO_PATIENT_ID = "DEMO-PT-001"
DEMO_PATIENT_IDENTIFIER = "PT-2026-0042"


def _dt(year, month, day, hour=9, minute=0):
    return datetime(year, month, day, hour, minute, tzinfo=timezone.utc)


def get_demo_patient():
    return {
        "id": DEMO_PATIENT_ID,
        "identifier": DEMO_PATIENT_IDENTIFIER,
        "age": 67,
        "sex": "Male",
        "major_conditions": [
            "Type 2 Diabetes Mellitus",
            "Chronic Kidney Disease (Stage 3)",
            "Hypertension",
            "Community-Acquired Pneumonia (resolved)"
        ],
        "current_admission": None,
        "created_at": _dt(2026, 1, 12),
        "updated_at": _dt(2026, 8, 14)
    }


def get_demo_documents():
    return [
        {
            "id": "DOC-001",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "gp_consultation_jan2026.txt",
            "document_type": "clinical_note",
            "document_date": _dt(2026, 1, 12),
            "title": "GP Consultation — January 2026",
            "source_author": "Dr. Sarah Patel",
            "source_institution": "Westfield Surgery",
            "processed": True,
            "raw_text": """GP CLINICAL NOTE
Date: 12 January 2026
Patient: PT-2026-0042 | Age: 67 | Male
Clinician: Dr. Sarah Patel — Westfield Surgery

PRESENTING COMPLAINT:
Routine review. Fatigue, increased thirst, polyuria for 3 months.

HISTORY:
No previous diagnosis of diabetes. Family history: father had Type 2 Diabetes.
Background hypertension, well controlled on Lisinopril 5mg OD for 4 years.

ALLERGIES:
Penicillin — rash (documented 2018)

EXAMINATION:
BP 138/82, HR 78, Weight 92kg, BMI 31.2
No peripheral oedema. Cardiovascular exam unremarkable.

INVESTIGATIONS:
HbA1c: 68 mmol/mol (diabetic range)
Fasting glucose: 9.2 mmol/L
U&E: Creatinine 112 µmol/L, eGFR 52 mL/min — CKD Stage 3
Urine PCR: 45 mg/mmol — significant proteinuria

ASSESSMENT:
1. New diagnosis: Type 2 Diabetes Mellitus
2. Chronic Kidney Disease Stage 3 — likely diabetic nephropathy
3. Hypertension — continue Lisinopril (renally protective)

PLAN:
- Start Metformin 500mg BD (with food)
- Continue Lisinopril 5mg OD
- Add Atorvastatin 40mg ON (cardiovascular risk)
- Refer to Nephrology for CKD management
- Diabetes education and dietary advice
- Repeat HbA1c in 3 months
- Review in 4 weeks

Dr. Sarah Patel, MBChB MRCGP""",
        },
        {
            "id": "DOC-002",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "nephrology_referral_feb2026.txt",
            "document_type": "referral_letter",
            "document_date": _dt(2026, 2, 28),
            "title": "Nephrology Referral — February 2026",
            "source_author": "Dr. Sarah Patel",
            "source_institution": "Westfield Surgery",
            "processed": True,
            "raw_text": """REFERRAL LETTER
Date: 28 February 2026
To: Nephrology Department, City Hospital
From: Dr. Sarah Patel, Westfield Surgery
Re: PT-2026-0042 | Age 67 | Male

Dear Colleague,

I am writing to refer this 67-year-old gentleman for specialist review and ongoing management of Chronic Kidney Disease Stage 3.

BACKGROUND:
Newly diagnosed with Type 2 Diabetes Mellitus in January 2026. Background hypertension for 4+ years.

RELEVANT INVESTIGATIONS:
- HbA1c 68 mmol/mol (Jan 2026)
- Creatinine 112 µmol/L, eGFR 52 mL/min (Jan 2026)
- Urine PCR 45 mg/mmol — significant proteinuria (Jan 2026)

CURRENT MEDICATIONS:
- Metformin 500mg BD
- Lisinopril 5mg OD
- Atorvastatin 40mg ON

ALLERGIES: Penicillin allergy (rash, 2018)

SPECIFIC QUESTIONS:
1. Confirmation of CKD staging and aetiology
2. Guidance on safe use of Metformin given declining renal function
3. Optimisation of renal protection strategy
4. Monitoring plan

I would be grateful for your review and advice.

Yours sincerely,
Dr. Sarah Patel
Westfield Surgery""",
        },
        {
            "id": "DOC-003",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "nephrology_clinic_note_apr2026.txt",
            "document_type": "specialist_note",
            "document_date": _dt(2026, 4, 15),
            "title": "Nephrology Clinic Note — April 2026",
            "source_author": "Dr. Mohammed Al-Rashid",
            "source_institution": "City Hospital Nephrology",
            "processed": True,
            "raw_text": """NEPHROLOGY OUTPATIENT CLINIC NOTE
Date: 15 April 2026
Patient: PT-2026-0042 | Age 67 | Male
Consultant: Dr. Mohammed Al-Rashid — City Hospital Nephrology

REASON FOR REVIEW:
New referral for CKD Stage 3 management and diabetic nephropathy.

HISTORY:
T2DM diagnosed January 2026. Hypertension 4+ years. CKD Stage 3 on bloods.

EXAMINATION:
BP 145/88 (borderline — review antihypertensive)
No significant peripheral oedema.

INVESTIGATIONS REVIEWED:
- Creatinine 112 µmol/L, eGFR 52 mL/min (Jan 2026)
- Urine PCR 45 mg/mmol

ASSESSMENT:
CKD Stage 3b likely secondary to diabetic nephropathy. Hypertension contributing factor.

PLAN:
1. Continue Lisinopril — increase dose to 10mg OD for improved renal protection
2. Metformin — continue but caution if eGFR falls below 45
3. Repeat U&E, HbA1c, urine PCR in 6 weeks
4. Target BP <130/80
5. Renal dietitian referral
6. Follow-up in 6 months

NOTE: The patient mentioned he has no known drug allergies when asked today. 
This was recorded in the clinic note but has not been formally updated.

Dr. Mohammed Al-Rashid, MD FRCP (Nephrology)""",
        },
        {
            "id": "DOC-004",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "gp_followup_jun2026.txt",
            "document_type": "clinical_note",
            "document_date": _dt(2026, 6, 10),
            "title": "GP Follow-Up — June 2026",
            "source_author": "Dr. Sarah Patel",
            "source_institution": "Westfield Surgery",
            "processed": True,
            "raw_text": """GP FOLLOW-UP NOTE
Date: 10 June 2026
Patient: PT-2026-0042 | Age 67 | Male
Clinician: Dr. Sarah Patel

REVIEW:
Follow-up post-nephrology appointment.

ALLERGIES:
Penicillin — rash (documented 2018) — unchanged

RECENT INVESTIGATIONS:
HbA1c: 59 mmol/mol (Jun 2026) — improving
Creatinine: 124 µmol/L, eGFR 47 mL/min — slight deterioration
Urine PCR: 52 mg/mmol — slightly increased proteinuria

MEDICATION REVIEW:
- Metformin 500mg BD: Continue — eGFR 47, still above threshold
- Lisinopril: Nephrology advised increase to 10mg — dose increased today
- Atorvastatin 40mg ON: Continue

ASSESSMENT:
Diabetes improving with dietary changes. Renal function mildly declining — within expected range for CKD Stage 3.
BP 135/82 — borderline.

PLAN:
Continue current management. Repeat bloods in 3 months.
Annual retinal screening arranged.
Flu vaccination given.

Dr. Sarah Patel""",
        },
        {
            "id": "DOC-005",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "ed_clerking_aug2026.txt",
            "document_type": "admission_summary",
            "document_date": _dt(2026, 8, 2),
            "title": "Emergency Admission Clerking — August 2026",
            "source_author": "Dr. James Chen",
            "source_institution": "City Hospital ED",
            "processed": True,
            "raw_text": """EMERGENCY DEPARTMENT CLERKING
Date: 02 August 2026 | Time: 14:32
Patient: PT-2026-0042 | Age 67 | Male
Admitting Doctor: Dr. James Chen — ED Senior Registrar

PRESENTING COMPLAINT:
5-day history of productive cough (yellow-green sputum), fever (home thermometer 38.9°C), progressive dyspnoea. Initially managed in community, worsening despite oral antibiotics (amoxicillin — prescribed by out-of-hours GP).

ALLERGIES:
No known drug allergies (as stated by patient — not formally reconciled with GP record)

PAST MEDICAL HISTORY:
1. Type 2 Diabetes Mellitus
2. Chronic Kidney Disease Stage 3
3. Hypertension

CURRENT MEDICATIONS (as stated by patient):
- Metformin 500mg BD
- Lisinopril 10mg OD
- Atorvastatin 40mg ON

EXAMINATION:
Temp 38.7°C, HR 104, RR 22, BP 128/74, SpO2 92% on air → 97% on 2L O2
Chest: Dullness and bronchial breathing right base. Creps bilateral.

INVESTIGATIONS:
CXR: Right lower lobe consolidation — consistent with pneumonia
WCC: 18.2 × 10^9/L (neutrophilia)
CRP: 287 mg/L
Creatinine: 198 µmol/L (↑ from baseline 124 — AKI)
Urea: 11.4 mmol/L
K+: 5.1 mmol/L

ASSESSMENT:
1. Community-acquired pneumonia (CAP) — moderate severity (CURB-65: 2)
2. Acute kidney injury (AKI Stage 1) on background CKD Stage 3

PLAN:
- Admit under medical team
- IV Co-amoxiclav 1.2g TDS (CAP protocol)
- HOLD Metformin — AKI
- HOLD Lisinopril — AKI + haemodynamic instability
- IV fluids
- Monitor U&E daily
- Blood cultures

NOTE: Patient reported no drug allergies. GP record previously documented Penicillin allergy. 
Co-amoxiclav commenced — clinical decision made that benefit outweighs risk pending allergy clarification.

Dr. James Chen, MBChB""",
        },
        {
            "id": "DOC-006",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "lab_results_aug2026.txt",
            "document_type": "lab_result",
            "document_date": _dt(2026, 8, 5),
            "title": "Laboratory Results — August 2026 (Admission)",
            "source_author": "City Hospital Laboratory",
            "source_institution": "City Hospital",
            "processed": True,
            "raw_text": """LABORATORY RESULTS REPORT
Date: 02–14 August 2026
Patient: PT-2026-0042

U&E TREND:
02 Aug: Na 138, K 5.1, Creatinine 198, Urea 11.4, eGFR 28 [AKI Stage 1]
04 Aug: Na 137, K 5.3, Creatinine 256, Urea 13.1, eGFR 20 [AKI Stage 2]
07 Aug: Na 140, K 4.8, Creatinine 287, Urea 14.2, eGFR 18 [AKI Stage 2 — peak]
10 Aug: Na 139, K 4.6, Creatinine 265, Urea 12.8, eGFR 20 [Improving]
12 Aug: Na 140, K 4.4, Creatinine 234, Urea 11.2, eGFR 23 [Improving]
14 Aug: Na 141, K 4.3, Creatinine 201, Urea 10.1, eGFR 28 [Partial recovery]

INFLAMMATORY MARKERS:
02 Aug: CRP 287, WCC 18.2
05 Aug: CRP 198, WCC 14.1
08 Aug: CRP 87, WCC 10.2
12 Aug: CRP 45, WCC 8.7

BLOOD CULTURES (02 Aug): No growth at 5 days.

HbA1c (02 Aug): 61 mmol/mol

NOTE: Creatinine has not returned to baseline (124 µmol/L pre-admission).
Ongoing CKD management required post-discharge. Nephrology review recommended.

Reference: CKD baseline Cr 124 µmol/L (Jun 2026)""",
        },
        {
            "id": "DOC-007",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "chest_xray_aug2026.txt",
            "document_type": "imaging_report",
            "document_date": _dt(2026, 8, 8),
            "title": "Chest X-Ray Report — August 2026",
            "source_author": "Dr. Lisa Wong",
            "source_institution": "City Hospital Radiology",
            "processed": True,
            "raw_text": """RADIOLOGY REPORT — CHEST X-RAY (PA)
Date: 08 August 2026
Patient: PT-2026-0042
Requesting Clinician: Dr. James Chen
Reporting Radiologist: Dr. Lisa Wong

CLINICAL INDICATION:
Day 6 chest X-ray for community-acquired pneumonia. Assess for resolution.

FINDINGS:
Compared with admission CXR (02 Aug 2026):
- Improving right lower lobe consolidation. Significantly less dense than previous.
- No new consolidation, effusion, or pneumothorax.
- Cardiac silhouette normal size.
- Bony thorax unremarkable.

IMPRESSION:
Improving right lower lobe consolidation. Clinical and radiological improvement consistent with responding pneumonia.

RECOMMENDATION:
Repeat CT chest recommended in 6 weeks following discharge to ensure complete resolution and exclude underlying malignancy given age >60 and significant consolidation.

Dr. Lisa Wong, FRCR
City Hospital Radiology
08 August 2026""",
        },
        {
            "id": "DOC-008",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "ward_progress_notes_aug2026.txt",
            "document_type": "clinical_note",
            "document_date": _dt(2026, 8, 10),
            "title": "Ward Progress Notes — August 2026",
            "source_author": "Medical Ward Team",
            "source_institution": "City Hospital",
            "processed": True,
            "raw_text": """WARD PROGRESS NOTES
Patient: PT-2026-0042

DAY 5 (07 Aug 2026 — Dr. A. Kumar):
Clinically improving. Still febrile 37.8°C. Renal function worsening — Cr 287 (peak).
Decision: Step-down to oral Co-amoxiclav 625mg TDS. Continue IV fluids.
Metformin remains HELD — renal function not recovered.
Lisinopril remains HELD.
Note: Consider nephrology consult given significant AKI on CKD background.

DAY 7 (09 Aug 2026 — Dr. A. Kumar):
Apyrexial for 48h. HR 82, BP 132/78. SpO2 97% on air.
Renal function improving — Cr 265, trending down.
Chest: Reduced creps. Patient reports improved breathing.
CXR (08 Aug): Improved consolidation.

DAY 10 (12 Aug 2026 — Dr. J. Chen):
Clinically well. Ready for discharge planning.
Cr 234 — improving but not at baseline.
DECISION: Metformin to remain STOPPED at discharge — renal function not yet returned to baseline.
Lisinopril: Decision — restart at reduced dose 5mg OD post-discharge, with GP review.
Arrange GP follow-up for 2 weeks, repeat U&E.

NOTE: Nephrology review was discussed but not formally requested during this admission. 
The August nephrology referral status from April follow-up is unclear — outstanding.

Dr. J. Chen / Dr. A. Kumar""",
        },
        {
            "id": "DOC-009",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "discharge_summary_aug2026.txt",
            "document_type": "discharge_summary",
            "document_date": _dt(2026, 8, 14),
            "title": "Discharge Summary — August 2026",
            "source_author": "Dr. James Chen",
            "source_institution": "City Hospital",
            "processed": True,
            "raw_text": """DISCHARGE SUMMARY
Date of Discharge: 14 August 2026
Patient: PT-2026-0042 | Age 67 | Male
Admitting Consultant: Dr. M. Robinson (Medicine)
Discharge Doctor: Dr. James Chen

ADMISSION DATE: 02 August 2026
DISCHARGE DATE: 14 August 2026
LENGTH OF STAY: 12 days

DIAGNOSIS AT DISCHARGE:
1. Community-acquired pneumonia (resolved)
2. Acute kidney injury Stage 2 on background CKD Stage 3 — partial recovery
3. Type 2 Diabetes Mellitus
4. Hypertension

ALLERGIES: No known drug allergies.

HOSPITAL COURSE:
Admitted with community-acquired pneumonia. Treated with IV Co-amoxiclav (stepped down to oral Day 5). Clinical and radiological improvement. AKI developed during admission (Cr peak 287 µmol/L, baseline 124). Renal function partially recovered to Cr 201 at discharge (eGFR 28).

INVESTIGATIONS DURING ADMISSION:
- CXR: Resolving RLL consolidation
- CXR Day 8: Improving
- Peak CRP 287, normalising at discharge 45
- Peak Creatinine 287 µmol/L (Day 7)
- Discharge Creatinine 201 µmol/L
- Blood cultures: No growth
- HbA1c: 61 mmol/mol

PROCEDURES: None surgical.

MEDICATION CHANGES:
- Metformin 500mg BD: STOPPED — AKI during admission. Do not restart until renal function reviewed.
- Lisinopril: Restarted at 5mg OD (reduced from 10mg) — titrate as renal function recovers
- Co-amoxiclav 625mg TDS: Complete 7-day course (3 days remaining at discharge)
- Atorvastatin 40mg ON: Continue

DISCHARGE MEDICATIONS:
1. Lisinopril 5mg OD
2. Atorvastatin 40mg ON
3. Co-amoxiclav 625mg TDS (complete course)

FOLLOW-UP:
1. GP review in 2 weeks — repeat U&E, reassess Metformin restart
2. REPEAT CT CHEST in 6 weeks — to confirm complete resolution and exclude malignancy
3. Nephrology follow-up — outstanding, arrange via GP

OUTSTANDING:
- Renal function not at baseline — monitor and nephrology review
- Metformin restart decision pending renal recovery
- Repeat CT chest (6 weeks)

INFORMATION FOR GP:
Important: Creatinine at discharge 201 µmol/L, not at pre-admission baseline of 124. 
Metformin should NOT be restarted until eGFR confirmed >45.
Allergy documentation: patient denies Penicillin allergy. Previous GP record documents Penicillin allergy (rash 2018). Please clarify and formally reconcile before next antibiotic prescribing.

Dr. James Chen MBChB
City Hospital — Medical Ward 7
14 August 2026""",
        },
        {
            "id": "DOC-010",
            "patient_id": DEMO_PATIENT_ID,
            "filename": "gp_postdischarge_letter_sep2026.txt",
            "document_type": "clinical_note",
            "document_date": _dt(2026, 9, 2),
            "title": "GP Post-Discharge Review — September 2026",
            "source_author": "Dr. Sarah Patel",
            "source_institution": "Westfield Surgery",
            "processed": True,
            "raw_text": """GP POST-DISCHARGE REVIEW
Date: 02 September 2026
Patient: PT-2026-0042 | Age 67 | Male
Clinician: Dr. Sarah Patel

REVIEW:
2-week post-discharge review following City Hospital admission.

ALLERGIES:
Penicillin allergy (rash 2018) — documented. Awaiting formal reconciliation.
Note: Discharge summary states "No known drug allergies" — discrepancy noted, to be clarified.

SYMPTOMS:
Patient reports improved breathing, reduced cough. Fatigue persisting.

MEDICATIONS:
- Lisinopril 5mg OD (restarted post-discharge)
- Atorvastatin 40mg ON
- Co-amoxiclav course completed.
- Metformin: NOT restarted — renal function still impaired

U&E TODAY (02 Sep 2026):
Creatinine 189 µmol/L, eGFR 30 — still below pre-admission baseline (124).

ASSESSMENT:
Recovering from pneumonia. Renal function improving but not yet at baseline.
Metformin remains stopped — appropriate.

PLAN:
- Repeat U&E in 4 weeks
- REMINDER: CT chest due — 6-week follow-up (due approximately 25 September 2026)
- Nephrology referral status: Unclear — original referral Feb 2026, no response letter in records.
- Consider urgent nephrology review given AKI on CKD.

NOTE TO RECORD: CT chest not yet arranged — GP to action or confirm via radiology.

Dr. Sarah Patel""",
        },
    ]


def get_demo_encounters():
    return [
        {
            "id": "ENC-001", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 1, 12), "encounter_type": "GP consultation",
            "location": "Westfield Surgery", "clinician": "Dr. Sarah Patel",
            "summary": "New diagnosis of Type 2 Diabetes and CKD Stage 3. Medications commenced."
        },
        {
            "id": "ENC-002", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 2, 28), "encounter_type": "Referral",
            "location": "Westfield Surgery", "clinician": "Dr. Sarah Patel",
            "summary": "Nephrology referral made for CKD management."
        },
        {
            "id": "ENC-003", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 4, 15), "encounter_type": "Specialist clinic",
            "location": "City Hospital Nephrology", "clinician": "Dr. Mohammed Al-Rashid",
            "summary": "Nephrology review. Lisinopril dose increased. Follow-up arranged."
        },
        {
            "id": "ENC-004", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 6, 10), "encounter_type": "GP follow-up",
            "location": "Westfield Surgery", "clinician": "Dr. Sarah Patel",
            "summary": "HbA1c improving. Renal function stable. Lisinopril increased to 10mg."
        },
        {
            "id": "ENC-005", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 8, 2), "encounter_type": "Emergency admission",
            "location": "City Hospital ED", "clinician": "Dr. James Chen",
            "summary": "Admitted with community-acquired pneumonia. AKI on background CKD."
        },
        {
            "id": "ENC-006", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 8, 14), "encounter_type": "Inpatient discharge",
            "location": "City Hospital Ward 7", "clinician": "Dr. James Chen",
            "summary": "Discharged after 12-day admission. Metformin stopped. CT chest recommended."
        },
        {
            "id": "ENC-007", "patient_id": DEMO_PATIENT_ID,
            "encounter_date": _dt(2026, 9, 2), "encounter_type": "GP follow-up",
            "location": "Westfield Surgery", "clinician": "Dr. Sarah Patel",
            "summary": "Post-discharge review. Renal function improving but not at baseline. CT not yet arranged."
        },
    ]


def get_demo_clinical_events():
    return [
        {
            "id": "EVT-001", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-001",
            "source_document_id": "DOC-001", "event_type": "diagnosis",
            "event_date": _dt(2026, 1, 12), "title": "New diagnosis: Type 2 Diabetes Mellitus",
            "description": "HbA1c 68 mmol/mol. Fasting glucose 9.2 mmol/L.", "clinical_significance": "high",
            "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-002", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-001",
            "source_document_id": "DOC-001", "event_type": "diagnosis",
            "event_date": _dt(2026, 1, 12), "title": "Diagnosis: CKD Stage 3",
            "description": "Creatinine 112 µmol/L, eGFR 52 mL/min. Significant proteinuria (PCR 45 mg/mmol).",
            "clinical_significance": "high", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-003", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-001",
            "source_document_id": "DOC-001", "event_type": "medication_start",
            "event_date": _dt(2026, 1, 12), "title": "Medication started: Metformin 500mg BD",
            "description": "Started for newly diagnosed Type 2 Diabetes.", "clinical_significance": "medium",
            "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-004", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-001",
            "source_document_id": "DOC-001", "event_type": "medication_start",
            "event_date": _dt(2026, 1, 12), "title": "Medication started: Atorvastatin 40mg ON",
            "description": "Started for cardiovascular risk reduction.", "clinical_significance": "medium",
            "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-005", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-002",
            "source_document_id": "DOC-002", "event_type": "referral",
            "event_date": _dt(2026, 2, 28), "title": "Referral: Nephrology",
            "description": "GP referral to nephrology for CKD Stage 3 management and diabetic nephropathy.",
            "clinical_significance": "medium", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-006", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-003",
            "source_document_id": "DOC-003", "event_type": "medication_change",
            "event_date": _dt(2026, 4, 15), "title": "Medication change: Lisinopril dose increased to 10mg",
            "description": "Nephrology recommendation: increase Lisinopril from 5mg to 10mg OD for improved renal protection.",
            "clinical_significance": "medium", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-007", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-005",
            "source_document_id": "DOC-005", "event_type": "admission",
            "event_date": _dt(2026, 8, 2), "title": "Emergency admission: Community-acquired pneumonia",
            "description": "Admitted with 5-day history of productive cough, fever 38.9°C, dyspnoea. CXR confirmed RLL consolidation.",
            "clinical_significance": "high", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-008", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-005",
            "source_document_id": "DOC-005", "event_type": "diagnosis",
            "event_date": _dt(2026, 8, 2), "title": "AKI Stage 1 on background CKD",
            "description": "Creatinine 198 µmol/L on admission (baseline 124). AKI in context of sepsis and CAP.",
            "clinical_significance": "high", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-009", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-005",
            "source_document_id": "DOC-006", "event_type": "result",
            "event_date": _dt(2026, 8, 7), "title": "Peak creatinine: 287 µmol/L (AKI Stage 2)",
            "description": "Creatinine peaked at 287 µmol/L on Day 7. AKI Stage 2. eGFR 18 mL/min.",
            "clinical_significance": "high", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-010", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-005",
            "source_document_id": "DOC-008", "event_type": "medication_stop",
            "event_date": _dt(2026, 8, 2), "title": "Medication stopped: Metformin",
            "description": "Metformin held on admission due to AKI. Stopped at discharge — renal function not at baseline.",
            "clinical_significance": "high", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-011", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-006",
            "source_document_id": "DOC-009", "event_type": "discharge",
            "event_date": _dt(2026, 8, 14), "title": "Discharge after 12-day admission",
            "description": "Discharged with resolving pneumonia. Creatinine 201 at discharge (not at baseline). CT chest recommended in 6 weeks.",
            "clinical_significance": "high", "is_confirmed": True, "confidence": 1.0
        },
        {
            "id": "EVT-012", "patient_id": DEMO_PATIENT_ID, "encounter_id": "ENC-007",
            "source_document_id": "DOC-010", "event_type": "result",
            "event_date": _dt(2026, 9, 2), "title": "Post-discharge U&E: Creatinine 189 µmol/L",
            "description": "Creatinine 189, eGFR 30. Improving but not at pre-admission baseline (124). Metformin remains stopped.",
            "clinical_significance": "medium", "is_confirmed": True, "confidence": 1.0
        },
    ]


def get_demo_conditions():
    return [
        {
            "id": "COND-001", "patient_id": DEMO_PATIENT_ID, "name": "Type 2 Diabetes Mellitus",
            "status": "active", "onset_date": _dt(2026, 1, 12), "source_document_id": "DOC-001"
        },
        {
            "id": "COND-002", "patient_id": DEMO_PATIENT_ID, "name": "Chronic Kidney Disease Stage 3",
            "status": "active", "onset_date": _dt(2026, 1, 12), "source_document_id": "DOC-001"
        },
        {
            "id": "COND-003", "patient_id": DEMO_PATIENT_ID, "name": "Hypertension",
            "status": "active", "onset_date": None, "source_document_id": "DOC-001"
        },
        {
            "id": "COND-004", "patient_id": DEMO_PATIENT_ID, "name": "Community-Acquired Pneumonia",
            "status": "resolved", "onset_date": _dt(2026, 8, 2),
            "resolved_date": _dt(2026, 8, 14), "source_document_id": "DOC-009"
        },
        {
            "id": "COND-005", "patient_id": DEMO_PATIENT_ID, "name": "Acute Kidney Injury Stage 2",
            "status": "resolved", "onset_date": _dt(2026, 8, 4),
            "resolved_date": _dt(2026, 8, 14),
            "notes": "Partial recovery only — creatinine not at baseline at discharge.",
            "source_document_id": "DOC-009"
        },
    ]


def get_demo_medications():
    return [
        {
            "id": "MED-001", "patient_id": DEMO_PATIENT_ID, "name": "Metformin",
            "dose": "500mg", "route": "oral", "frequency": "twice daily",
            "status": "stopped", "start_date": _dt(2026, 1, 12), "stop_date": _dt(2026, 8, 2),
            "stop_reason": "Acute kidney injury during admission. Do not restart until eGFR confirmed >45.",
            "source_document_id": "DOC-009"
        },
        {
            "id": "MED-002", "patient_id": DEMO_PATIENT_ID, "name": "Lisinopril",
            "dose": "5mg", "route": "oral", "frequency": "once daily",
            "status": "active", "start_date": None,
            "source_document_id": "DOC-009"
        },
        {
            "id": "MED-003", "patient_id": DEMO_PATIENT_ID, "name": "Atorvastatin",
            "dose": "40mg", "route": "oral", "frequency": "once nightly",
            "status": "active", "start_date": _dt(2026, 1, 12),
            "source_document_id": "DOC-001"
        },
    ]


def get_demo_medication_changes():
    return [
        {
            "id": "MEDCHG-001", "medication_id": "MED-002",
            "change_date": _dt(2026, 4, 15), "change_type": "dose_changed",
            "previous_value": "5mg OD", "new_value": "10mg OD",
            "reason": "Nephrology recommendation: improve renal protection",
            "source_document_id": "DOC-003"
        },
        {
            "id": "MEDCHG-002", "medication_id": "MED-002",
            "change_date": _dt(2026, 8, 14), "change_type": "dose_changed",
            "previous_value": "10mg OD", "new_value": "5mg OD",
            "reason": "AKI during admission — reduced dose at discharge, titrate as renal function recovers",
            "source_document_id": "DOC-009"
        },
        {
            "id": "MEDCHG-003", "medication_id": "MED-001",
            "change_date": _dt(2026, 8, 2), "change_type": "medication_stopped",
            "previous_value": "Active — 500mg BD", "new_value": "Stopped",
            "reason": "Acute kidney injury during admission",
            "source_document_id": "DOC-008"
        },
    ]


def get_demo_open_loops():
    return [
        {
            "id": "LOOP-001", "patient_id": DEMO_PATIENT_ID,
            "title": "Repeat CT Chest",
            "description": "Repeat CT chest recommended 6 weeks post-discharge to confirm consolidation resolution and exclude malignancy.",
            "loop_type": "investigation",
            "status": "open",
            "requested_date": _dt(2026, 8, 14),
            "source_document_id": "DOC-007",
            "evidence_text": "Repeat CT chest recommended in 6 weeks following discharge to ensure complete resolution and exclude underlying malignancy given age >60 and significant consolidation.",
            "latest_matching_record": "None found in available records",
            "action_required": "Verify whether repeat CT chest has been arranged and completed. Due approximately 25 September 2026."
        },
        {
            "id": "LOOP-002", "patient_id": DEMO_PATIENT_ID,
            "title": "Nephrology Follow-Up",
            "description": "Nephrology referral made February 2026. No specialist response documented in available records. Further follow-up noted as outstanding at discharge August 2026.",
            "loop_type": "referral",
            "status": "open",
            "requested_date": _dt(2026, 2, 28),
            "source_document_id": "DOC-002",
            "evidence_text": "Nephrology follow-up — outstanding, arrange via GP (Discharge Summary, 14 Aug 2026). Nephrology referral status: Unclear — original referral Feb 2026, no response letter in records (GP note, 02 Sep 2026).",
            "latest_matching_record": "Nephrology clinic attendance Apr 2026 (DOC-003) — but subsequent follow-up not documented",
            "action_required": "Verify current nephrology follow-up status. Acute deterioration in renal function during admission may require urgent review."
        },
        {
            "id": "LOOP-003", "patient_id": DEMO_PATIENT_ID,
            "title": "Metformin Restart Decision",
            "description": "Metformin stopped during admission due to AKI. Discharge instructions state not to restart until eGFR confirmed >45. No subsequent restart documented in available records.",
            "loop_type": "medication_review",
            "status": "open",
            "requested_date": _dt(2026, 8, 14),
            "source_document_id": "DOC-009",
            "evidence_text": "Do not restart Metformin until renal function reviewed. Repeat U&E in 2 weeks. (Discharge Summary, 14 Aug 2026). Post-discharge creatinine 189 µmol/L, eGFR 30 — still below threshold. (GP note, 02 Sep 2026).",
            "latest_matching_record": "GP review 02 Sep 2026 — eGFR 30, Metformin remains stopped",
            "action_required": "Monitor renal function. Restart Metformin only when eGFR confirmed >45. Diabetes management plan needed in the interim."
        },
        {
            "id": "LOOP-004", "patient_id": DEMO_PATIENT_ID,
            "title": "Post-Discharge Renal Function Monitoring",
            "description": "Repeat U&E recommended at 2-week post-discharge review and 4-weekly thereafter. Creatinine still elevated at last check (02 Sep 2026).",
            "loop_type": "investigation",
            "status": "open",
            "requested_date": _dt(2026, 9, 2),
            "source_document_id": "DOC-010",
            "evidence_text": "Repeat U&E in 4 weeks (GP note, 02 Sep 2026). Creatinine 189, eGFR 30 — improving but not at baseline.",
            "latest_matching_record": "U&E 02 Sep 2026 — Creatinine 189, eGFR 30",
            "action_required": "Next U&E due approximately 30 September 2026. Assess Lisinopril titration and Metformin restart at that review."
        },
    ]


def get_demo_conflicts():
    return [
        {
            "id": "CONF-001", "patient_id": DEMO_PATIENT_ID,
            "title": "Penicillin Allergy — Conflicting Documentation",
            "description": "GP records consistently document a Penicillin allergy (rash, 2018). Hospital discharge summary states 'No known drug allergies'. Conflict not formally resolved in available records.",
            "conflict_type": "allergy",
            "severity": "high",
            "source_a_document_id": "DOC-001",
            "source_b_document_id": "DOC-009",
            "source_a_text": "ALLERGIES: Penicillin — rash (documented 2018) — GP Clinical Note, 12 Jan 2026",
            "source_b_text": "ALLERGIES: No known drug allergies — Discharge Summary, 14 Aug 2026",
            "action_required": "Verify Penicillin allergy status before any antibiotic prescribing. Formal allergy reconciliation required. Note: Co-amoxiclav (penicillin-containing) was administered during August 2026 admission.",
            "resolved": False
        },
        {
            "id": "CONF-002", "patient_id": DEMO_PATIENT_ID,
            "title": "Lisinopril Dose — Inconsistency Across Records",
            "description": "Nephrology note (Apr 2026) documented Lisinopril increased to 10mg OD. Discharge summary (Aug 2026) records discharge on Lisinopril 5mg OD — reduced due to AKI. GP post-discharge note records 5mg OD. The sequence is clinically logical but the dose change is not consistently documented across records.",
            "conflict_type": "dose",
            "severity": "low",
            "source_a_document_id": "DOC-003",
            "source_b_document_id": "DOC-009",
            "source_a_text": "Increase Lisinopril to 10mg OD — Nephrology Clinic Note, 15 Apr 2026",
            "source_b_text": "Lisinopril 5mg OD (discharge) — Discharge Summary, 14 Aug 2026",
            "action_required": "The dose reduction at discharge is clinically explained by AKI. Ensure current dose (5mg) and plan to titrate are documented and communicated clearly.",
            "resolved": False
        },
        {
            "id": "CONF-003", "patient_id": DEMO_PATIENT_ID,
            "title": "Metformin Status — Active vs Stopped",
            "description": "GP follow-up note (Jun 2026) records Metformin as active (500mg BD). Ward progress notes (Aug 2026) and discharge summary confirm Metformin stopped. Earlier documents (Sep 2026 GP note) confirm it remains stopped. The conflict exists between pre- and post-admission records.",
            "conflict_type": "medication",
            "severity": "medium",
            "source_a_document_id": "DOC-004",
            "source_b_document_id": "DOC-009",
            "source_a_text": "Metformin 500mg BD: Continue — eGFR 47, still above threshold — GP Note, 10 Jun 2026",
            "source_b_text": "Metformin 500mg BD: STOPPED — AKI during admission. Do not restart until renal function reviewed — Discharge Summary, 14 Aug 2026",
            "action_required": "Current status: Metformin STOPPED (confirmed post-discharge). Any medication reconciliation system or summary listing medications as of Jun 2026 should be updated to reflect current stopped status.",
            "resolved": False
        },
    ]


def get_demo_detected_changes():
    return [
        {
            "id": "CHG-001", "patient_id": DEMO_PATIENT_ID,
            "change_type": "medication_stopped", "title": "Metformin stopped",
            "entity_name": "Metformin", "previous_state": "Active — 500mg BD",
            "current_state": "Stopped", "change_date": _dt(2026, 8, 2),
            "reason": "Acute kidney injury during admission",
            "source_document_id": "DOC-008",
            "evidence_text": "Metformin to remain STOPPED at discharge — renal function not yet returned to baseline."
        },
        {
            "id": "CHG-002", "patient_id": DEMO_PATIENT_ID,
            "change_type": "worsening", "title": "Significant creatinine rise — AKI Stage 2",
            "entity_name": "Creatinine", "previous_state": "124 µmol/L (Jun 2026)",
            "current_state": "287 µmol/L peak (Aug 2026) — 201 µmol/L at discharge",
            "change_date": _dt(2026, 8, 7),
            "reason": "Acute kidney injury in context of sepsis and pneumonia",
            "source_document_id": "DOC-006",
            "evidence_text": "Peak Creatinine 287 µmol/L (Day 7). AKI Stage 2. eGFR 18 mL/min."
        },
        {
            "id": "CHG-003", "patient_id": DEMO_PATIENT_ID,
            "change_type": "new_admission", "title": "Emergency hospital admission",
            "entity_name": "Hospital admission", "previous_state": "Community",
            "current_state": "Admitted — City Hospital (12 days)",
            "change_date": _dt(2026, 8, 2),
            "reason": "Community-acquired pneumonia",
            "source_document_id": "DOC-005",
            "evidence_text": "Admitted 02 August 2026 with community-acquired pneumonia."
        },
        {
            "id": "CHG-004", "patient_id": DEMO_PATIENT_ID,
            "change_type": "dose_changed", "title": "Lisinopril dose reduced",
            "entity_name": "Lisinopril", "previous_state": "10mg OD",
            "current_state": "5mg OD", "change_date": _dt(2026, 8, 14),
            "reason": "AKI during admission — reduced dose at discharge",
            "source_document_id": "DOC-009",
            "evidence_text": "Lisinopril: Restarted at 5mg OD (reduced from 10mg) — titrate as renal function recovers."
        },
        {
            "id": "CHG-005", "patient_id": DEMO_PATIENT_ID,
            "change_type": "new_diagnosis", "title": "AKI Stage 2",
            "entity_name": "Acute Kidney Injury", "previous_state": "CKD Stage 3 (stable)",
            "current_state": "AKI Stage 2 on CKD background — partial recovery",
            "change_date": _dt(2026, 8, 4),
            "reason": "Sepsis/pneumonia-related AKI",
            "source_document_id": "DOC-006",
            "evidence_text": "04 Aug: Creatinine 256, eGFR 20 [AKI Stage 2]"
        },
        {
            "id": "CHG-006", "patient_id": DEMO_PATIENT_ID,
            "change_type": "improving", "title": "CRP improving — infection responding",
            "entity_name": "CRP", "previous_state": "287 mg/L (admission)",
            "current_state": "45 mg/L (discharge)",
            "change_date": _dt(2026, 8, 12),
            "reason": None,
            "source_document_id": "DOC-006",
            "evidence_text": "CRP: 287 mg/L (admission) → 45 mg/L (discharge)"
        },
    ]


def get_demo_investigations():
    return [
        {
            "id": "INV-001", "patient_id": DEMO_PATIENT_ID, "name": "HbA1c",
            "investigation_type": "blood", "requested_date": _dt(2026, 1, 12),
            "result_date": _dt(2026, 1, 12), "status": "completed",
            "source_document_id": "DOC-001"
        },
        {
            "id": "INV-002", "patient_id": DEMO_PATIENT_ID, "name": "U&E / Creatinine",
            "investigation_type": "blood", "requested_date": _dt(2026, 1, 12),
            "result_date": _dt(2026, 9, 2), "status": "completed",
            "source_document_id": "DOC-010"
        },
        {
            "id": "INV-003", "patient_id": DEMO_PATIENT_ID, "name": "Repeat CT Chest",
            "investigation_type": "imaging", "requested_date": _dt(2026, 8, 8),
            "result_date": None, "status": "pending",
            "source_document_id": "DOC-007"
        },
        {
            "id": "INV-004", "patient_id": DEMO_PATIENT_ID, "name": "Chest X-Ray",
            "investigation_type": "imaging", "requested_date": _dt(2026, 8, 2),
            "result_date": _dt(2026, 8, 8), "status": "completed",
            "source_document_id": "DOC-007"
        },
        {
            "id": "INV-005", "patient_id": DEMO_PATIENT_ID, "name": "Blood Cultures",
            "investigation_type": "microbiology", "requested_date": _dt(2026, 8, 2),
            "result_date": _dt(2026, 8, 7), "status": "completed",
            "source_document_id": "DOC-006"
        },
        {
            "id": "INV-006", "patient_id": DEMO_PATIENT_ID, "name": "Urine PCR",
            "investigation_type": "urine", "requested_date": _dt(2026, 1, 12),
            "result_date": _dt(2026, 1, 12), "status": "completed",
            "source_document_id": "DOC-001"
        },
    ]
