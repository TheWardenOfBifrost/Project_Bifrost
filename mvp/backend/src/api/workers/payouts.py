# src/api/workers/payouts.py
import threading, time
from sqlmodel import Session, select
from ..deps import engine
from ..models import PayoutRequest, PayoutStatus

def _tick():
    # simple loop: approve -> sent -> confirmed
    while True:
        try:
            with Session(engine) as session:
                # move approved -> sent
                apr = session.exec(select(PayoutRequest).where(PayoutRequest.status == PayoutStatus.approved)).all()
                for pr in apr:
                    pr.status = PayoutStatus.sent
                    session.add(pr)
                session.commit()
                # move sent -> confirmed
                snd = session.exec(select(PayoutRequest).where(PayoutRequest.status == PayoutStatus.sent)).all()
                for pr in snd:
                    pr.status = PayoutStatus.confirmed
                    session.add(pr)
                session.commit()
        except Exception:
            pass
        time.sleep(5)

_worker_started = False
def start_worker_once():
    global _worker_started
    if _worker_started: return
    t = threading.Thread(target=_tick, daemon=True)
    t.start()
    _worker_started = True
