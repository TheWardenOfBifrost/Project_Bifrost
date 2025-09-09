# src/api/routers/balances.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from ..deps import get_session, get_current_user
from ..models import Asset, UserBalance, Scope
from ..services import accounting

router = APIRouter(prefix="/balances", tags=["balances"])

@router.get("")
def get_balances(session: Session = Depends(get_session), user=Depends(get_current_user)):
    assets = {a.id: a for a in session.exec(select(Asset)).all()}
    rows = session.exec(select(UserBalance).where(UserBalance.user_id == user.id)).all()
    out = []
    for r in rows:
        a = assets[r.asset_id]
        out.append({
            "asset": a.code,
            "locked": r.locked_amount,
            "unlocked": r.unlocked_amount,
            "decimals": a.decimals
        })
    return {"balances": out}

@router.post("/adjust")
def adjust_balance(payload: dict, session: Session = Depends(get_session), user=Depends(get_current_user)):
    # Admin-stub: vores dummy get_current_user giver dig admin-rettigheder
    asset = payload.get("asset", "STARS")
    scope = Scope(payload.get("scope", "unlocked"))
    delta = int(payload.get("delta_atomic", 0))
    bal_after = accounting.adjust(
        session,
        user_id=user.id,
        asset_code=asset,
        scope=scope,
        delta=delta,
        reason="admin_adjust"
    )
    return {"ok": True, "asset": asset, "scope": scope, "balance_after": bal_after}

