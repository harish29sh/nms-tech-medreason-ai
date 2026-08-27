#!/usr/bin/env bash
set -e
source .venv/bin/activate
docker compose up -d postgres
python scripts/bootstrap.py
echo "Open http://127.0.0.1:8000"
uvicorn app.main:app --host 127.0.0.1 --port 8000
