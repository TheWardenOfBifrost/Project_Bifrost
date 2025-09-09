# src/api/models.py
from __future__ import annotations
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Column, JSON

# --- Enums ---------------------------------------------------------

class AssetKind(str, Enum):
    coin = "coin"       # on-chain coins (STARS, ENJ, ATOM, etc.)
    soft = "soft"       # off-chain currency (DUST)
    craft = "craft"     # off-chain resource (SHARD)

class Scope(str, Enum):
    locked = "locked"
    unlocked = "unlocked"

class PayoutStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    sent = "sent"
    confirmed = "confirmed"
    failed = "failed"
    cancelled = "cancelled"

class ChainKind(str, Enum):
    EVM = "EVM"
    COSMOS = "COSMOS"
    ENJIN = "ENJIN"

# --- Core tables ---------------------------------------------------

class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    code: str = Field(index=True, unique=True)   # e.g. STARS, DUST, SHARD
    kind: AssetKind
    decimals: int = 6
    is_active: bool = True

class UserBalance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    locked_amount: int = 0        # store as integer “atomic units” (respect decimals)
    unlocked_amount: int = 0

class Ledger(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    scope: Scope = Field(default=Scope.unlocked)
    delta: int  # +/-
    balance_after: Optional[int] = None
    reason: str = Field(default="misc")
    ref_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ConversionRule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_asset_id: int = Field(foreign_key="asset.id", index=True)
    to_asset_id: int = Field(foreign_key="asset.id", index=True)
    rate_num: int = 1     # from * rate_num / rate_den = to
    rate_den: int = 1
    is_enabled: bool = True

# --- Wallet linking ------------------------------------------------

class WalletLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    chain: ChainKind
    address: str = Field(index=True)
    label: Optional[str] = None
    is_primary: bool = False
    verified_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class WalletChallenge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    chain: ChainKind
    address_hint: Optional[str] = None
    nonce: str = Field(index=True)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=10))
    used_at: Optional[datetime] = None

# --- Withdraw & DEX -----------------------------------------------

class PayoutRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    from_asset_id: int = Field(foreign_key="asset.id")
    to_asset_id: Optional[int] = Field(foreign_key="asset.id", default=None)  # None = same asset
    amount: int
    to_chain: ChainKind
    to_wallet_link_id: int = Field(foreign_key="walletlink.id")
    status: PayoutStatus = Field(default=PayoutStatus.pending)
    quoted_fee: Optional[int] = None
    slippage_bps: Optional[int] = None
    route_provider: Optional[str] = None
    tx_id: Optional[str] = Field(default=None, index=True)
    memo_tag: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DexRoute(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payout_id: int = Field(foreign_key="payoutrequest.id", index=True)
    provider: str
    route_json: dict = Field(sa_column=Column(JSON))
    min_out: Optional[int] = None
    deadline: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- Marketplace (stub) -------------------------------------------

class Market(str, Enum):
    market_locked = "locked"
    market_unlocked = "unlocked"

class MarketplaceListing(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    seller_id: int = Field(index=True)
    asset_id: int = Field(foreign_key="asset.id", index=True)
    amount: int
    price: int
    price_asset_id: int = Field(foreign_key="asset.id")
    market: Market
    status: str = Field(default="active")  # active|sold|cancelled
    created_at: datetime = Field(default_factory=datetime.utcnow)
