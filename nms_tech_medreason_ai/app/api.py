"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

from fastapi import APIRouter
from .schemas import AnalyzeRequest
from .safety import detect_red_flags, safety_prefix, validate_answer
from .clinical.encephalopathy import rank
from .rag.retriever import retrieve
from .llm import ask_ollama

router = APIRouter()

SYSTEM_PROMPT = """
You are MedReason AI, a clinical reasoning assistant for healthcare professionals.
You are not an autonomous diagnostic system.

Rules:
- Do not claim certainty.
- Do not invent patient findings.
- Do not invent references.
- Distinguish differential diagnosis from established diagnosis.
- Prioritize emergencies and reversible causes.
- Use retrieved context as evidence support.
- State when evidence was not verified.
- Do not reproduce copyrighted textbook passages.
- Do not provide a patient-specific prescription as if you were the treating clinician.
- Encourage local protocols and specialist escalation.
"""

@router.post("/analyze")
async def analyze(req: AnalyzeRequest):
    p = req.patient
    combined = "\n".join([
        f"Age: {p.age}", f"Sex: {p.sex}",
        f"Chief complaint: {p.chief_complaint}",
        f"Duration: {p.duration}",
        f"HPI: {p.history_of_presenting_illness}",
        f"Past medical history: {p.past_medical_history}",
        f"Past surgical history: {p.past_surgical_history}",
        f"Medications: {p.medication_history}",
        f"Allergies: {p.allergies}",
        f"Family history: {p.family_history}",
        f"Social history: {p.social_history}",
        f"Personal history: {p.personal_history}",
        f"Examination: {p.examination}",
        f"Vitals: {p.vitals}",
        f"Labs: {p.labs}",
        f"Cultures: {p.cultures}",
        f"Biopsy/pathology: {p.pathology_biopsy}",
        f"X-ray: {p.xray}",
        f"USG: {p.ultrasound}",
        f"CT: {p.ct}",
        f"MRI: {p.mri}",
        f"MRA: {p.mra}",
        f"MRV: {p.mrv}",
        f"Contrast: {p.contrast_details}",
        f"Other investigations: {p.other_investigations}",
        f"Question: {req.question}"
    ])

    flags = detect_red_flags(combined)
    is_encephalopathy = any(
        term in combined.lower()
        for term in ["encephalopathy", "altered sensorium", "altered mental status", "confusion", "drowsiness"]
    )

    differential = rank(combined) if is_encephalopathy else []
    refs = retrieve("clinical reasoning encephalopathy altered mental status safety guidelines", 5)

    diff_text = "\n".join(
        f"- {x['diagnosis']} ({x['priority']}): {x['supporting']}"
        for x in differential[:8]
    )
    ref_text = "\n".join(
        f"[{r['id']}] {r['title']} — {r['organization']} — {r['url']}"
        for r in refs
    )

    prompt = f"""
PATIENT DATA
{combined}

STRUCTURED DIFFERENTIAL CANDIDATES
{diff_text}

REFERENCE REGISTRY
{ref_text}

Produce:
1. Problem representation
2. Immediate safety concerns
3. Prioritized differential
4. Key missing history
5. Focused examination
6. Suggested investigations separated into immediate/basic/conditional
7. How results may change the differential
8. High-level management considerations
9. References using ONLY the supplied reference IDs
10. Uncertainty

For CT/MRI/MRA/MRV with or without contrast, explain that modality and contrast selection depend on the clinical question, contraindications, renal function/other relevant factors and local radiology protocol. Do not invent an indication.
"""

    answer = validate_answer(safety_prefix(flags) + await ask_ollama(SYSTEM_PROMPT, prompt))

    suggested = []
    if is_encephalopathy:
        suggested = [
            "Immediate clinical assessment and vital signs.",
            "Check capillary glucose promptly.",
            "Focused neurological examination and mental-status/GCS assessment.",
            "Basic laboratory evaluation guided by the presentation.",
            "Targeted microbiology, neuroimaging, CSF studies, EEG or toxicology only when clinically indicated.",
            "Use local emergency and specialty protocols."
        ]

    return {
        "emergency_flags": flags,
        "differential": differential[:8],
        "suggested_evaluation": suggested,
        "answer": answer,
        "citations": refs,
        "disclaimer": "Prototype only. Not validated for clinical diagnosis or treatment; clinician judgment and current local guidance remain essential."
    }
