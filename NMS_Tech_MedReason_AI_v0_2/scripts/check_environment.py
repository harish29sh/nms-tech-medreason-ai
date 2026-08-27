"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
import asyncio,httpx
from app.config import settings
from app.database import db_available

async def main():
    print("Database:","OK" if db_available() else "NOT AVAILABLE")
    async with httpx.AsyncClient(timeout=5) as client:
        try:
            r=await client.get(f"{settings.ollama_base_url}/api/tags"); print("Ollama:","OK" if r.is_success else f"HTTP {r.status_code}")
        except Exception as e: print("Ollama: NOT AVAILABLE",e)
    print("LLM model:",settings.ollama_model); print("Embedding model:",settings.embed_model)
if __name__=="__main__": asyncio.run(main())
