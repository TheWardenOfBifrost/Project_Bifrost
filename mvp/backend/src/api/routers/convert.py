# src/api/routers/convert.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from ..deps import get_session, get_current_user
from ..services import conversion

router = APIRouter(prefix="/convert", tags=["convert"])

@router.post("")
def post_convert(payload: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    fr = payload.get("from"); to = payload.get("to"); amt = int(payload.get("amount_atomic", 0))
    return {"detail": "Not implemented yet", "quote": conversion.quote(session, fr, to, amt)}
