# mvp/backend/run.ps1
$ErrorActionPreference = "Stop"
$env:PYTHONUNBUFFERED = "1"
uvicorn src.api.main:app --reload --port 8000
