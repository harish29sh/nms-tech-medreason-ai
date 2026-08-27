@echo off
setlocal
echo ===============================================
echo NMS Tech MedReason AI v0.2 - Windows Setup
echo ===============================================
where python >nul 2>&1 || (echo Python 3.11+ is required.& exit /b 1)
where ollama >nul 2>&1 || (echo Ollama is required: https://ollama.com/& exit /b 1)
where docker >nul 2>&1 || (echo Docker Desktop is required.& exit /b 1)
if not exist .venv python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
ollama pull qwen3:4b
ollama pull nomic-embed-text
docker compose up -d postgres
python scripts\bootstrap.py
echo Setup complete. Run run_windows.bat
endlocal
