from fastapi import FastAPI
from datetime import datetime

app = FastAPI(title="Bifrost MVP API")

STARTED_AT = datetime.utcnow().isoformat() + "Z"
API_VERSION = "0.1.0"

@app.get("/health")
def health():
    return {"ok": True, "service": "bifrost-mvp", "started_at": STARTED_AT}

@app.get("/version")
def version():
    return {"version": API_VERSION, "env": "dev"}
