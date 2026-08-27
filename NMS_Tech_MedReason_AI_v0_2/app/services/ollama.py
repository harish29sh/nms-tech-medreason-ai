"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
import httpx
from ..config import settings

async def chat(system_prompt,user_prompt):
    payload={"model":settings.ollama_model,"stream":False,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],"options":{"temperature":0.1}}
    async with httpx.AsyncClient(timeout=180) as client:
        r=await client.post(f"{settings.ollama_base_url}/api/chat",json=payload); r.raise_for_status(); return r.json()["message"]["content"]

async def embed(text):
    async with httpx.AsyncClient(timeout=120) as client:
        r=await client.post(f"{settings.ollama_base_url}/api/embed",json={"model":settings.embed_model,"input":text}); r.raise_for_status(); return r.json()["embeddings"][0]
