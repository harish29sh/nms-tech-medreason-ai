"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api import router

app = FastAPI(
    title="NMS Tech MedReason AI",
    version="0.1.0",
    description="Clinical reasoning prototype for healthcare professionals."
)

app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="web"), name="static")

@app.get("/")
def home():
    return FileResponse("web/index.html")
