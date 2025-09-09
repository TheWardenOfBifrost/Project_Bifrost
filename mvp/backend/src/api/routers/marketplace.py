# src/api/routers/marketplace.py
from fastapi import APIRouter
from ..services import marketplace

router = APIRouter(prefix="/marketplace", tags=["marketplace"])

@router.get("/locked")
def get_locked():
    return {"items": marketplace.list_locked(), "detail": "Marketplace (locked) coming soon"}

@router.get("/unlocked")
def get_unlocked():
    return {"items": marketplace.list_unlocked(), "detail": "Marketplace (unlocked) coming soon"}
