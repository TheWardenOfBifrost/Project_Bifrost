# src/api/adapters/chains_mock.py
import time, random
from .chains_base import ChainAdapter

class MockAdapter(ChainAdapter):
    def estimate_fee(self, asset_code: str, amount_atomic: int) -> int:
        return max(1, amount_atomic // 10000)
    def send(self, asset_code: str, to_address: str, amount_atomic: int, memo: str | None = None) -> str:
        return f"mocktx_{int(time.time())}_{random.randint(1000,9999)}"
    def get_tx_status(self, tx_id: str) -> str:
        return "confirmed"
