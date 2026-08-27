"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

from typing import Optional
from pydantic import BaseModel, Field

class PatientHistory(BaseModel):
    age: Optional[int] = Field(default=None, ge=0, le=130)
    sex: Optional[str] = None
    chief_complaint: str = ""
    duration: str = ""
    history_of_presenting_illness: str = ""
    past_medical_history: str = ""
    past_surgical_history: str = ""
    medication_history: str = ""
    allergies: str = ""
    family_history: str = ""
    social_history: str = ""
    personal_history: str = ""
    examination: str = ""
    vitals: str = ""
    labs: str = ""
    cultures: str = ""
    pathology_biopsy: str = ""
    xray: str = ""
    ultrasound: str = ""
    ct: str = ""
    mri: str = ""
    mra: str = ""
    mrv: str = ""
    contrast_details: str = ""
    other_investigations: str = ""

class AnalyzeRequest(BaseModel):
    patient: PatientHistory
    question: str = ""
