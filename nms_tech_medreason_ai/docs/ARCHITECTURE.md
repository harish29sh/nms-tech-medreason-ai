# Architecture

v0.1:
Web UI → FastAPI → structured clinical engine → local Ollama/Qwen3 → safety → references.

Production target:
Frontend → authentication/API gateway → patient-data minimization → clinical parser → syndrome classifier → rules/knowledge graph → hybrid RAG (keyword + vector) → reranker → LLM → citation verifier → safety validator → response.

The patient schema already accepts history, examination, laboratory, microbiology, pathology/biopsy, X-ray, USG, CT, MRI, MRA, MRV and contrast information.

For production, add structured fields for specimen, organism, antimicrobial susceptibility, pathology diagnosis, imaging modality/protocol, date/time and source.

Do not ingest copyrighted textbooks unless the intended use is licensed.
