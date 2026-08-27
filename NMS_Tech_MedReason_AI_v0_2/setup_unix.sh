#!/usr/bin/env bash
set -e
command -v python3 >/dev/null || { echo "Python 3.11+ required"; exit 1; }
command -v ollama >/dev/null || { echo "Ollama required: https://ollama.com/"; exit 1; }
command -v docker >/dev/null || { echo "Docker required"; exit 1; }
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
[ -f .env ] || cp .env.example .env
ollama pull qwen3:4b
ollama pull nomic-embed-text
docker compose up -d postgres
python scripts/bootstrap.py
echo "Setup complete. Run ./run_unix.sh"
