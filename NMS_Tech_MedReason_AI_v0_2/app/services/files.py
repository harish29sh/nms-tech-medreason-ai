"""NMS Tech Proprietary Material. Copyright © 2026 NMS Tech."""
from pathlib import Path
import json
ROOT = Path(__file__).resolve().parents[2]

def load_json(rel_path: str):
    return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))

def load_modules():
    return load_json("knowledge/complaints.json")

def load_sources():
    return load_json("knowledge/sources.json")
