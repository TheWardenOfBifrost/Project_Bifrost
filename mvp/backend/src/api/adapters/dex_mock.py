# src/api/adapters/dex_base.py
from typing import Protocol

class DexAdapter(Protocol):
    def quote(self, from_asset: str, to_asset: str, amount_atomic: int) -> dict: ...
    def swap_and_send(self, from_asset: str, to_asset: str, amount_atomic: int, to_address: str, slippage_bps: int = 50) -> str: ...

# src/api/adapters/dex_mock.py
from .dex_base import DexAdapter

class MockDex(DexAdapter):
    def quote(self, from_asset: str, to_asset: str, amount_atomic: int) -> dict:
        return {"provider": "mockdex", "min_out": amount_atomic, "fee": 0}
    def swap_and_send(self, from_asset: str, to_asset: str, amount_atomic: int, to_address: str, slippage_bps: int = 50) -> str:
        return f"mockdex_tx_{from_asset}_{to_asset}_{amount_atomic}"
