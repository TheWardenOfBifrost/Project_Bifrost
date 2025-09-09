# src/api/services/accounting.py
from sqlmodel import Session, select
from ..models import UserBalance, Asset, Ledger, Scope

def _get_asset(session: Session, code: str) -> Asset:
    return session.exec(select(Asset).where(Asset.code == code)).first()

def adjust(session: Session, *, user_id: int, asset_code: str, scope: Scope, delta: int, reason: str, ref_id: str | None = None) -> int:
    asset = _get_asset(session, asset_code)
    if not asset:
        raise ValueError("Unknown asset")
    ub = session.exec(
        select(UserBalance).where(UserBalance.user_id == user_id, UserBalance.asset_id == asset.id)
    ).first()
    if not ub:
        ub = UserBalance(user_id=user_id, asset_id=asset.id)
        session.add(ub)
    if scope == Scope.locked:
        new_bal = ub.locked_amount + delta
        if new_bal < 0: raise ValueError("Insufficient locked balance")
        ub.locked_amount = new_bal
        bal_after = new_bal
    else:
        new_bal = ub.unlocked_amount + delta
        if new_bal < 0: raise ValueError("Insufficient unlocked balance")
        ub.unlocked_amount = new_bal
        bal_after = new_bal
    session.add(Ledger(user_id=user_id, asset_id=asset.id, scope=scope, delta=delta, balance_after=bal_after, reason=reason, ref_id=ref_id))
    session.commit()
    session.refresh(ub)
    return bal_after
