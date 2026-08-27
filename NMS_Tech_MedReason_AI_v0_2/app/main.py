"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .api import router
from .config import settings

app=FastAPI(title=settings.app_name,version=settings.app_version,description="NMS Tech clinician-facing clinical reasoning prototype.")
app.include_router(router,prefix="/api")
app.mount("/static",StaticFiles(directory="web"),name="static")

@app.get("/")
def home():
    return FileResponse("web/index.html")
