"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

DIFFERENTIALS = [
    {
        "diagnosis": "Metabolic encephalopathy",
        "priority": "high",
        "supporting": "Consider glucose, sodium, calcium, renal, hepatic, acid-base and other systemic abnormalities.",
        "initial_evaluation": ["Capillary blood glucose", "Electrolytes", "Renal function", "Liver profile", "CBC"]
    },
    {
        "diagnosis": "Toxic/drug-related encephalopathy",
        "priority": "high",
        "supporting": "Review prescribed medicines, dose changes, recreational exposures and poisoning risk.",
        "initial_evaluation": ["Medication reconciliation", "Exposure history", "Targeted toxicology when clinically indicated"]
    },
    {
        "diagnosis": "Infectious encephalopathy / meningoencephalitis",
        "priority": "high",
        "supporting": "Fever, headache, meningism, seizures, focal deficits or immunocompromise increase concern.",
        "initial_evaluation": ["Vitals", "CBC and appropriate cultures", "Neuroimaging and CSF evaluation when clinically indicated"]
    },
    {
        "diagnosis": "Structural/vascular CNS disease",
        "priority": "high",
        "supporting": "Focal neurological findings, trauma, sudden onset or severe headache raise concern.",
        "initial_evaluation": ["Urgent neuroimaging when indicated", "Neurological examination"]
    },
    {
        "diagnosis": "Seizure-related / postictal state",
        "priority": "moderate",
        "supporting": "Witnessed seizure, tongue injury, incontinence, postictal confusion or recurrent episodes.",
        "initial_evaluation": ["Seizure history", "Neurological examination", "EEG when clinically indicated"]
    },
    {
        "diagnosis": "Hypoxic encephalopathy",
        "priority": "high",
        "supporting": "Hypoxemia, respiratory failure, cardiac arrest or severe circulatory compromise.",
        "initial_evaluation": ["SpO2", "Respiratory assessment", "ABG/VBG where appropriate"]
    },
    {
        "diagnosis": "Hepatic encephalopathy",
        "priority": "moderate",
        "supporting": "Known liver disease or features suggesting hepatic dysfunction.",
        "initial_evaluation": ["History/examination for liver disease", "Liver profile", "Renal function", "Electrolytes", "Precipitant search"]
    },
    {
        "diagnosis": "Uremic encephalopathy",
        "priority": "moderate",
        "supporting": "Advanced renal dysfunction or uremic symptoms.",
        "initial_evaluation": ["Renal function", "Electrolytes", "Volume status", "Dialysis history"]
    },
]

def rank(history_text):
    text = history_text.lower()
    scored = []
    for item in DIFFERENTIALS:
        score = 0
        if item["diagnosis"].startswith("Metabolic") and any(x in text for x in ["diabetes", "glucose", "sodium", "renal", "electrolyte"]):
            score += 3
        if "infectious" in item["diagnosis"].lower() and any(x in text for x in ["fever", "infection", "mening", "headache"]):
            score += 3
        if "toxic" in item["diagnosis"].lower() and any(x in text for x in ["drug", "overdose", "poison", "tablet"]):
            score += 3
        if "structural" in item["diagnosis"].lower() and any(x in text for x in ["stroke", "trauma", "focal", "headache"]):
            score += 3
        if "seizure" in item["diagnosis"].lower() and "seiz" in text:
            score += 3
        if "hypoxic" in item["diagnosis"].lower() and any(x in text for x in ["hypoxia", "low oxygen", "respiratory failure"]):
            score += 3
        if "hepatic" in item["diagnosis"].lower() and any(x in text for x in ["liver", "cirrhosis", "jaundice"]):
            score += 3
        if "uremic" in item["diagnosis"].lower() and any(x in text for x in ["kidney", "uremia", "dialysis"]):
            score += 3
        scored.append({**item, "score": score})
    return sorted(scored, key=lambda x: (x["score"], x["priority"] == "high"), reverse=True)
