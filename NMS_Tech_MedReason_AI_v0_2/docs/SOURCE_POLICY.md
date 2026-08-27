# Medical Source and RAG Policy

External medical sources are **link-only** by default. Only entries marked `rag_ingestion_allowed: true` in `knowledge/sources.json` may be ingested without a separate licence review. The default v0.2 vector corpus contains NMS-owned/original structured clinical summaries.

Before external ingestion, document the rightsholder, licence/version, commercial-use permission, redistribution permission, RAG/ML permission if relevant, required attribution, review/expiry date and exact document/version checksum.

A public URL does not automatically mean its content can be copied into a RAG database.
