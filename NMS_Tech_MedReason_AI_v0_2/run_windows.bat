@echo off
setlocal
if not exist .venv (echo Run setup_windows.bat first.& exit /b 1)
call .venv\Scripts\activate.bat
docker compose up -d postgres
python scripts\bootstrap.py
start "" http://127.0.0.1:8000
uvicorn app.main:app --host 127.0.0.1 --port 8000
endlocal
