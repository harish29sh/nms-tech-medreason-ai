"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
def imaging_safety_note(text):
    lower=text.lower()
    if not any(x in lower for x in ["x-ray","xray","ultrasound","usg","ct","mri","mra","mrv","contrast","dye"]): return ""
    return "Imaging safety: modality, protocol, and contrast choice must follow the specific clinical question, patient factors, contraindications, renal function/contrast risk when relevant, pregnancy status when relevant, and the local radiology protocol. Use current condition-specific imaging guidance."
