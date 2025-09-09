# src/api/routers/wallets.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..deps import get_session, get_current_user
from ..models import WalletLink, WalletChallenge, ChainKind
from datetime import datetime
import secrets

router = APIRouter(prefix="/wallets", tags=["wallets"])

@router.get("")
def list_wallets(session: Session = Depends(get_session), user=Depends(get_current_user)):
    rows = session.exec(select(WalletLink).where(WalletLink.user_id == user.id)).all()
    return {"wallets": rows}

@router.post("/link/start")
def link_start(payload: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    chain = ChainKind(payload.get("chain", "EVM"))
    address = payload.get("address", "")
    nonce = secrets.token_urlsafe(16)
    ch = WalletChallenge(user_id=user.id, chain=chain, address_hint=address[:8]+"..." if address else None, nonce=nonce)
    session.add(ch); session.commit(); session.refresh(ch)
    message = f"""Bifrost Wallet Link
User: {user.id}
Chain: {chain}
Nonce: {nonce}
Expires: {ch.expires_at.isoformat()}"""
    return {"challenge_id": ch.id, "message": message}

@router.post("/link/verify")
def link_verify(payload: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    challenge_id = payload.get("challenge_id")
    address = payload.get("address")
    signature = payload.get("signature")  # TODO: verify by chain
    ch = session.get(WalletChallenge, challenge_id)
    if not ch or ch.user_id != user.id or ch.used_at or ch.expires_at < datetime.utcnow():
        return {"ok": False, "detail": "Invalid/expired challenge"}
    # STUB: accept any signature for now
    wl = session.exec(select(WalletLink).where(WalletLink.user_id==user.id, WalletLink.address==address)).first()
    if not wl:
        wl = WalletLink(user_id=user.id, chain=ch.chain, address=address, verified_at=datetime.utcnow())
        session.add(wl)
    else:
        wl.verified_at = datetime.utcnow()
    ch.used_at = datetime.utcnow()
    session.commit(); session.refresh(wl)
    return {"ok": True, "wallet": wl}
