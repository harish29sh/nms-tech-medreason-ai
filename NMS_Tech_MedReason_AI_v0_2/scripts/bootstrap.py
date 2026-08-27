"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
import asyncio
from app.database import initialize_database,SessionLocal
from app.models import Source,KnowledgeChunk
from app.services.files import load_sources,load_modules
from app.services.ollama import embed

def module_to_content(module):
    return "\n".join([f"Specialty: {module['specialty']}",f"Syndrome: {module['syndrome']}","Aliases: "+", ".join(module["aliases"]),"Red flags: "+"; ".join(module["red_flags"]),"Differential diagnoses: "+"; ".join(d["name"] for d in module["differentials"]),"Key history: "+"; ".join(module["key_history_questions"]),"Focused examination: "+"; ".join(module["focused_examination"]),"Initial evaluation: "+"; ".join(module["initial_evaluation"])])

async def main():
    print("Initializing PostgreSQL/pgvector...")
    initialize_database()
    with SessionLocal() as db:
        for s in load_sources():
            existing=db.get(Source,s["id"]); payload=dict(s)
            if existing:
                existing.title=s["title"]; existing.organization=s["organization"]; existing.url=s["url"]; existing.source_type=s["source_type"]; existing.verified_on=s["verified_on"]; existing.reuse_policy=s["reuse_policy"]; existing.rag_ingestion_allowed=s["rag_ingestion_allowed"]; existing.metadata_json=payload
            else:
                db.add(Source(id=s["id"],title=s["title"],organization=s["organization"],url=s["url"],source_type=s["source_type"],verified_on=s["verified_on"],reuse_policy=s["reuse_policy"],rag_ingestion_allowed=s["rag_ingestion_allowed"],metadata_json=payload))
        db.commit()
    print("Embedding NMS-owned clinical modules...")
    for module in load_modules():
        content=module_to_content(module); chunk_id=f"NMS-{module['id']}-V02"; vector=None
        try: vector=await embed(content)
        except Exception as exc: print(f"Embedding unavailable for {module['id']}: {exc}")
        with SessionLocal() as db:
            chunk=db.get(KnowledgeChunk,chunk_id)
            if chunk:
                chunk.title=module["syndrome"]; chunk.content=content; chunk.source_ids=module["reference_ids"]
                if vector is not None: chunk.embedding=vector
            else:
                db.add(KnowledgeChunk(id=chunk_id,module_id=module["id"],specialty=module["specialty"],title=module["syndrome"],content=content,source_ids=module["reference_ids"],embedding=vector))
            db.commit()
        print(f"  ✓ {module['id']}")
    print("Bootstrap complete.")

if __name__=="__main__": asyncio.run(main())
