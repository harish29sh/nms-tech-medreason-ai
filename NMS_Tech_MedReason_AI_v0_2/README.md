# NMS Tech MedReason AI v0.2

**Copyright © 2026 NMS Tech. All Rights Reserved.**

A local-first clinical reasoning prototype for healthcare professionals.

## Included in v0.2

- FastAPI backend
- Local Qwen3 (`qwen3:4b`) through Ollama
- PostgreSQL + pgvector
- Local `nomic-embed-text` embeddings
- Real vector RAG over NMS-owned/original clinical knowledge chunks
- 29 complaint/syndrome modules across Medicine, Surgery, Emergency, OBG and Pediatrics
- Comprehensive HPI, past/personal/family/drug/allergy/social history capture
- General and systemic examination capture
- CBC, glucose, electrolytes, renal/liver/coagulation/inflammatory/endocrine/cardiac/ABG-VBG/urine fields
- Blood, urine, sputum and CSF cultures plus PCR/serology
- Biopsy/histopathology and cytology
- ECG, X-ray, USG, CT, MRI, MRA, MRV and contrast/dye notes
- Deterministic complaint-to-differential engine
- Emergency red-flag detector
- Numeric medication-dose safety guard
- Citation whitelist that removes invented source IDs
- Official external reference registry
- Browser UI
- Windows/macOS/Linux setup scripts
- GitHub CI and tests

## Medical-source rule

Official guideline portals are **link-only by default**. Their protected text is not scraped or embedded. Only NMS-owned/original content is ingested into pgvector unless a separate licence review permits additional ingestion.

Do not add Harrison's, Bailey & Love, or other copyrighted textbook PDFs without appropriate permission/licensing.

## Quick start — Windows

Install:
1. Python 3.11+
2. Ollama: https://ollama.com/
3. Docker Desktop

Then unzip the project, open the folder in VS Code and double-click or run:

```bat
setup_windows.bat
run_windows.bat
```

Open `http://127.0.0.1:8000`.

## Quick start — macOS/Linux

```bash
chmod +x setup_unix.sh run_unix.sh
./setup_unix.sh
./run_unix.sh
```

## Manual start

```bash
python -m venv .venv
# activate .venv
pip install -r requirements.txt
cp .env.example .env
ollama pull qwen3:4b
ollama pull nomic-embed-text
docker compose up -d postgres
python scripts/bootstrap.py
uvicorn app.main:app --reload
```

## How RAG works

`python scripts/bootstrap.py` creates PostgreSQL/pgvector tables, loads the source registry, turns each NMS clinical module into an original knowledge chunk, obtains a local embedding from Ollama, and stores the vector. At question time the query is embedded and nearest chunks are retrieved. If DB/embeddings are unavailable, the deterministic module provides fallback context.

## Reference registry

The default registry includes link-only references to:
- American College of Radiology Appropriateness Criteria
- ACR Altered Mental Status imaging criteria
- IDSA Practice Guidelines
- AHA/ASA Guidelines and Statements
- ACOG Clinical Guidance
- AAP Clinical Practice Guidelines
- NICE Guidance
- WHO AI governance guidance
- CDSCO Medical Device Software guidance

The app does not imply that these organizations endorse NMS Tech.

## Tests

```bash
pytest -q
```

## GitHub upload

Create a **private** repository such as `nms-tech-medreason-ai`, then from this exact project folder:

```bash
git init
git add README.md LICENSE COPYRIGHT.md NOTICE.md DISCLAIMER.md SECURITY.md CONTRIBUTING.md THIRD_PARTY_NOTICES.md requirements.txt pyproject.toml docker-compose.yml .env.example .gitignore app web knowledge scripts tests docs .github setup_windows.bat run_windows.bat setup_unix.sh run_unix.sh
git commit -m "NMS Tech MedReason AI v0.2"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nms-tech-medreason-ai.git
git push -u origin main
```

Avoid `git add .` if the containing folder has unrelated or private files.

## Regulatory/clinical status

This is a development prototype, not a validated autonomous diagnostic or treatment system. Review `DISCLAIMER.md`, `docs/CLINICAL_VALIDATION.md`, and current applicable regulatory requirements before real-world clinical deployment.
