# src/api/services/conversion.py
from sqlmodel import Session
from ..models import ConversionRule

def quote(session: Session, from_code: str, to_code: str, amount_atomic: int) -> dict:
    # TODO: real lookup; stub returns 1:1
    return {"rate_num": 1, "rate_den": 1, "out": amount_atomic}

def convert(session: Session, user_id: int, from_code: str, to_code: str, amount_atomic: int) -> dict:
    # TODO: use accounting.adjust twice
    return {"detail": "Not implemented yet"}
