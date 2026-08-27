"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
import re
EMERGENCY_PATTERNS={
"Potential airway/breathing emergency":[r"\bstridor\b",r"\brespiratory distress\b",r"\bcyanosis\b",r"\bapnoea\b",r"\bunresponsive\b",r"\bspo2\s*[<≤]\s*90"],
"Potential circulatory emergency":[r"\bshock\b",r"\bhypotension\b",r"\bmajor bleeding\b",r"\bpoor perfusion\b"],
"Potential neurologic emergency":[r"\bstatus epilepticus\b",r"\bcoma\b",r"\bhemiplegia\b",r"\bhemiparesis\b",r"\baphasia\b",r"\bnew focal\b",r"\bthunderclap\b"],
"Potential metabolic emergency":[r"\bhypoglyc",r"\bglucose\s*[<≤]\s*70\b"],
"Potential severe infection":[r"\bseptic shock\b",r"\bmeningism\b",r"\bneck stiffness\b"]}
DOSE_PATTERN=re.compile(r"\b\d+(?:\.\d+)?\s*(?:mg|mcg|µg|g|ml|mL|units?|IU)\b",re.I)

def detect_emergency_flags(text):
    return [label for label,patterns in EMERGENCY_PATTERNS.items() if any(re.search(p,text,re.I) for p in patterns)]

def emergency_preamble(flags):
    return "" if not flags else "SAFETY ALERT: Potential emergency features are present. Prioritize immediate clinician assessment, ABCs, vital signs, reversible causes and local emergency/escalation pathways. Do not delay care for this AI output.\n\n"

def strip_unverified_doses(answer):
    kept=[]; removed=False
    for line in answer.splitlines():
        if DOSE_PATTERN.search(line):
            kept.append("[Medication dose removed by NMS safety validator: use a verified drug/dose source and local protocol.]"); removed=True
        else: kept.append(line)
    return "\n".join(kept),removed
