"""
NMS Tech Proprietary Material
Copyright © 2026 NMS Tech. All Rights Reserved.

This file contains original NMS Tech project material. Unauthorized copying,
redistribution, republication, or commercial use is prohibited without prior
written authorization from NMS Tech.

Third-party libraries, frameworks, models, medical references, and standards
remain subject to their respective licences and ownership rights.
"""

from .references import search_references

def retrieve(query, limit=5):
    # v0.1: reference registry retrieval.
    # Production: document ingestion + chunking + embeddings + pgvector + reranking.
    return search_references(query, limit)
