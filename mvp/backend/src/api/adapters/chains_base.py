# src/api/adapters/chains_base.py
from typing import Protocol

class ChainAdapter(Protocol):
    def estimate_fee(self, asset_code: str, amount_atomic: int) -> int: ...
    def send(self, asset_code: str, to_address: str, amount_atomic: int, memo: str | None = None) -> str: ...
    def get_tx_status(self, tx_id: str) -> str: ...  # pending|confirmed|failed
