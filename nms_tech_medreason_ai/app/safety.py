"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

import re

EMERGENCY_PATTERNS = {
    "possible ABC/emergency": [
        r"\bsevere dyspnea\b", r"\brespiratory distress\b", r"\bshock\b",
        r"\bhypotension\b", r"\bSpO2\s*[<≤]\s*90", r"\bunresponsive\b"
    ],
    "possible acute neurologic emergency": [
        r"\bnew focal deficit\b", r"\bhemiparesis\b", r"\bhemiplegia\b",
        r"\bnew seizure\b", r"\bstatus epilepticus\b", r"\bcoma\b",
        r"\bsudden severe headache\b", r"\bintracranial hemorrhage\b"
    ],
    "possible serious infection/CNS infection": [
        r"\bmeningism\b", r"\bneck stiffness\b", r"\bmeningitis\b",
        r"\bencephalitis\b", r"\bsepsis\b"
    ],
    "possible severe metabolic emergency": [
        r"\bhypoglyc", r"\bglucose\s*[<≤]\s*70\b",
        r"\bsevere hyperkal", r"\bsevere hyponat"
    ],
}

def detect_red_flags(text: str):
    flags = []
    for label, patterns in EMERGENCY_PATTERNS.items():
        if any(re.search(p, text, re.I) for p in patterns):
            flags.append(label)
    return flags

def safety_prefix(flags):
    if not flags:
        return ""
    return (
        "SAFETY ALERT: Potential emergency features were detected. "
        "Prioritize immediate clinical assessment, ABCs, vital signs, "
        "reversible causes and local emergency protocols. "
        "Do not delay escalation for the AI response.\n\n"
    )

def validate_answer(answer):
    if any(x in answer.lower() for x in ["definitively diagnosed", "100% diagnosis", "certainly has"]):
        answer += "\n\nSafety note: diagnostic certainty must be established by the treating clinician."
    return answer
