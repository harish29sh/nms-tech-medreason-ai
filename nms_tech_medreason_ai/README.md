# NMS Tech MedReason AI — Clinical Reasoning Prototype

Proprietary NMS Tech research/education prototype for healthcare professionals.

## What it includes
- Patient history: demographics, chief complaint, HPI, past history, surgery, medicines, allergies, family/social/personal history
- Examination and vitals
- Blood tests, cultures, biopsy/pathology
- X-ray, USG, CT, MRI, MRA, MRV and contrast details
- Encephalopathy/altered-mental-status differential engine
- Local Qwen3 through Ollama
- RAG-style reference registry
- Emergency/red-flag safety layer
- FastAPI backend and web UI
- PostgreSQL + pgvector Docker option

## Important
This is a prototype, not a validated medical device and not a substitute for clinical judgment.
Use synthetic/de-identified cases only.
Do not add copyrighted textbook PDFs unless you have the necessary licence.

## Run
1. Install Python 3.11+
2. Install Ollama from https://ollama.com/
3. Run: `ollama pull qwen3:8b`
4. Create venv:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
   - Linux/macOS: `python3 -m venv .venv` then `source .venv/bin/activate`
5. `pip install -r requirements.txt`
6. `uvicorn app.main:app --reload`
7. Open http://127.0.0.1:8000

If your computer cannot run 8B, change OLLAMA_MODEL in `.env` to a smaller Qwen3 model.

SQLite is used for zero-setup v0.1. The included Docker Compose file provides PostgreSQL + pgvector for the next stage.


## Copyright and Ownership

Copyright © 2026 NMS Tech. All Rights Reserved.

Original NMS Tech source code, project-specific architecture, prompts, documentation,
workflow logic, UI materials, and other original repository materials are
proprietary. Unauthorized copying, redistribution, republication, or commercial
use is prohibited without prior written authorization from NMS Tech.

Third-party frameworks, models, libraries, medical references, standards, and
other external works remain subject to their own licences and ownership rights.

See `LICENSE`, `COPYRIGHT.md`, `NOTICE.md`, and `THIRD_PARTY_NOTICES.md`.
