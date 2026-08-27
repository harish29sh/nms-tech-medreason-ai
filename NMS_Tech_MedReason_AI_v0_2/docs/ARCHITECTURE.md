# NMS Tech MedReason AI v0.2 Architecture

Browser UI → FastAPI → case normalization → emergency safety detector + complaint/syndrome classifier + deterministic differential ranking → RAG retrieval (NMS original chunks + Ollama embeddings + PostgreSQL/pgvector) → local Qwen3 → medication-dose guard + citation whitelist + imaging safety → clinician-facing response.

External guidelines are link-only in the default build. Their protected text is not copied into the vector database.
