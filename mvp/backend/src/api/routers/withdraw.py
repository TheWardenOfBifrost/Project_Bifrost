# src/api/routers/withdraw.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..deps import get_session, get_current_user
from ..models import PayoutRequest, PayoutStatus, WalletLink, Asset, ChainKind
from datetime import datetime

router = APIRouter(prefix="/withdraw", tags=["withdraw"])

@router.post("/quote")
def quote(payload: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    # STUB: constant fee
    return {"network_fee": 10, "service_fee": 0, "eta_sec": 10, "dex_quote": None}

@router.post("/request")
def request_withdraw(payload: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    from_code = payload["from_asset"]
    to_code = payload.get("to_asset")  # optional
    amount = int(payload["amount_atomic"])
    wl_id = int(payload["wallet_link_id"])
    wl = session.get(WalletLink, wl_id)
    if not wl or wl.user_id != user.id or not wl.verified_at:
        return {"ok": False, "detail": "Invalid wallet"}
    from_asset = session.exec(select(Asset).where(Asset.code==from_code)).first()
    to_asset = session.exec(select(Asset).where(Asset.code==to_code)).first() if to_code else None
    pr = PayoutRequest(
        user_id=user.id,
        from_asset_id=from_asset.id,
        to_asset_id=to_asset.id if to_asset else None,
        amount=amount,
        to_chain=wl.chain,
        to_wallet_link_id=wl.id,
        status=PayoutStatus.pending,
        quoted_fee=10
    )
    session.add(pr); session.commit(); session.refresh(pr)
    return {"ok": True, "payout_id": pr.id, "status": pr.status}

@router.get("")
def list_withdraws(session: Session = Depends(get_session), user=Depends(get_current_user)):
    rows = session.exec(select(PayoutRequest).where(PayoutRequest.user_id == user.id).order_by(PayoutRequest.id.desc())).all()
    return {"items": rows}

@router.get("/{payout_id}")
def get_withdraw(payout_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    pr = session.get(PayoutRequest, payout_id)
    if not pr or pr.user_id != user.id:
        return {"detail": "Not found"}
    return pr

# Admin approve (keep your existing admin auth; stub here)
@router.post("/{payout_id}/approve")
def approve_withdraw(payout_id: int, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if not user.is_admin:
        return {"detail": "forbidden"}
    pr = session.get(PayoutRequest, payout_id)
    if not pr: return {"detail": "not found"}
    pr.status = PayoutStatus.approved
    pr.updated_at = datetime.utcnow()
    session.add(pr); session.commit()
    return {"ok": True, "status": pr.status}
