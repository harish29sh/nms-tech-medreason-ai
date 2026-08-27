"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
import re
from .files import load_sources
SOURCES={s["id"]:s for s in load_sources()}
CITATION_RE=re.compile(r"\[([A-Z0-9][A-Z0-9\-]{2,})\]")

def sources_for_ids(ids):
    seen=set(); out=[]
    for sid in ids:
        if sid in SOURCES and sid not in seen:
            out.append(SOURCES[sid]); seen.add(sid)
    return out

def validate_citations(answer,allowed_ids):
    allowed=set(allowed_ids); found=CITATION_RE.findall(answer); invalid=sorted({x for x in found if x not in allowed}); clean=answer
    for bad in invalid: clean=clean.replace(f"[{bad}]","[UNVERIFIED-CITATION-REMOVED]")
    return clean,invalid
