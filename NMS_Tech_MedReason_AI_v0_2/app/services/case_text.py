"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
def patient_to_text(patient) -> str:
    lines=[]
    for key,value in patient.model_dump().items():
        if value not in (None, ""):
            lines.append(f"{key.replace('_',' ').title()}: {value}")
    return "\n".join(lines)
