"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
from sqlalchemy import select
from ..database import SessionLocal
from ..models import KnowledgeChunk
from .ollama import embed
from .clinical_engine import module_context

async def retrieve(query,module_id,top_k=5):
    try:
        vector=await embed(query)
        with SessionLocal() as db:
            stmt=select(KnowledgeChunk).where(KnowledgeChunk.embedding.is_not(None)).order_by(KnowledgeChunk.embedding.cosine_distance(vector)).limit(top_k)
            rows=db.execute(stmt).scalars().all()
            if rows:
                return [{"id":r.id,"title":r.title,"content":r.content,"source_ids":r.source_ids,"score":None} for r in rows]
    except Exception:
        pass
    return module_context(module_id)
