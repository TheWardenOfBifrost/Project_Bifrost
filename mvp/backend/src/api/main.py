from fastapi import Query
from sqlalchemy import text
from src.api.db import engine
from fastapi import FastAPI, HTTPException, Query, Header
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Literal
import hashlib, secrets, re

app = FastAPI(title="Bifrost MVP API (Auth + Profile)")

# ====== IN-MEMORY STATE (nulstilles ved genstart) ======
players: Dict[str, Dict[str, int]] = {}       # key = email -> {"locked": int, "unlocked": int}
withdraw_requests: List[Dict] = []
request_auto_id = 1

# Auth & sessions
users: Dict[str, Dict] = {}                   # email -> {password_hash, created_at, profile:{xp,achievements,nfts}}
sessions: Dict[str, str] = {}                 # access_token -> email
remember_tokens: Dict[str, str] = {}          # long_token (remember me) -> email
password_resets: Dict[str, Dict] = {}         # reset_token -> {email, expires_at}

ADMIN_TOKEN = "secret123"
STARTED_AT = datetime.utcnow().isoformat() + "Z"
API_VERSION = "0.4.0"

# ====== MODELS ======
class RegisterBody(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class LoginBody(BaseModel):
    email: EmailStr
    password: str
    remember_me: bool = False

class ForgotPasswordBody(BaseModel):
    email: EmailStr

class ResetPasswordBody(BaseModel):
    token: str
    new_password: str = Field(min_length=6)

class F2PRequest(BaseModel):
    # player_id bliver din email; hvis du bruger token, er feltet valgfrit
    player_id: Optional[EmailStr] = None
    reward_locked: int = Field(10, ge=1)

class MatchResultRequest(BaseModel):
    player_id: Optional[EmailStr] = None
    locked_spent: int = Field(..., ge=1)
    result: Literal["win", "lose"]

class WithdrawRequest(BaseModel):
    player_id: Optional[EmailStr] = None
    amount: int = Field(..., ge=1)
    address: str

class AdminDecision(BaseModel):
    request_id: int = Field(..., ge=1)
    approve: bool
    admin_token: str

class ProfileProgress(BaseModel):
    add_xp: int = 0
    add_achievements: List[str] = []
    add_nfts: List[str] = []

# ====== HELPERS ======
def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def password_hash(pw: str) -> str:
    # MVP: ren sha256. (I produktion brug bcrypt/argon2.)
    return sha256(pw)

def verify_password(pw: str, ph: str) -> bool:
    return password_hash(pw) == ph

def parse_bearer(auth_header: Optional[str]) -> Optional[str]:
    if not auth_header:
        return None
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None

def get_or_create_player(email: str) -> Dict[str, int]:
    if email not in players:
        players[email] = {"locked": 0, "unlocked": 0}
    return players[email]

def get_user_or_404(email: str) -> Dict:
    u = users.get(email)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

def who_am_i(authorization: Optional[str]) -> str:
    """
    Returnerer email baseret på Authorization:
    - Bearer <access_token> (sessions)
    - Bearer remember:<remember_token> (konverteres til en ny access_token)
    """
    token = parse_bearer(authorization)
    if not token:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    # Remember-me path
    if token.startswith("remember:"):
        rtok = token.split("remember:", 1)[1]
        email = remember_tokens.get(rtok)
        if not email:
            raise HTTPException(status_code=401, detail="Invalid remember token")
        # udsted ny kort access token
        new_access = secrets.token_hex(16)
        sessions[new_access] = email
        # Returnér med speciel fejl så klient kan opdatere token hvis man vil
        raise HTTPException(status_code=498, detail={"msg": "Use new access token", "access_token": new_access})
    # Normal session
    email = sessions.get(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid or expired access token")
    return email

# ====== BASIC ======
@app.get("/health")
def health():
    return {"ok": True, "service": "bifrost-mvp", "started_at": STARTED_AT}

@app.get("/version")
def version():
    return {"version": API_VERSION, "env": "dev"}

# ====== AUTH ======
@app.post("/auth/register")
def register(body: RegisterBody):
    email = body.email.lower().strip()
    if email in users:
        raise HTTPException(status_code=409, detail="Email already registered")
    users[email] = {
        "password_hash": password_hash(body.password),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "profile": {"xp": 0, "achievements": [], "nfts": []},
    }
    # Opret balance
    get_or_create_player(email)
    return {"msg": "registered", "email": email}

@app.post("/auth/login")
def login(body: LoginBody):
    email = body.email.lower().strip()
    u = users.get(email)
    if not u or not verify_password(body.password, u["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = secrets.token_hex(16)
    sessions[access_token] = email
    result = {"msg": "logged_in", "email": email, "access_token": access_token}
    if body.remember_me:
        rtoken = secrets.token_hex(24)
        remember_tokens[rtoken] = email
        # i en rigtig app: sæt HttpOnly cookie. Her returnerer vi blot token-strengen.
        result["remember_token"] = rtoken
    return result

@app.post("/auth/forgot-password")
def forgot_password(body: ForgotPasswordBody):
    email = body.email.lower().strip()
    if email not in users:
        # For sikkerhed svarer man normalt “ok” uanset – vi gør det samme.
        return {"msg": "If the email exists, a reset link has been sent."}
    token = secrets.token_urlsafe(24)
    password_resets[token] = {"email": email, "expires_at": (datetime.utcnow() + timedelta(minutes=15))}
    # MVP: vi “sender” ikke mail – vi returnerer token så du kan teste reset.
    return {"msg": "reset_created", "reset_token_demo": token, "expires_in_minutes": 15}

@app.post("/auth/reset-password")
def reset_password(body: ResetPasswordBody):
    entry = password_resets.get(body.token)
    if not entry:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    if datetime.utcnow() > entry["expires_at"]:
        del password_resets[body.token]
        raise HTTPException(status_code=400, detail="Reset token expired")
    email = entry["email"]
    users[email]["password_hash"] = password_hash(body.new_password)
    del password_resets[body.token]
    return {"msg": "password_reset_ok", "email": email}

@app.get("/me")
def me(authorization: Optional[str] = Header(None, alias="Authorization")):
    email = who_am_i(authorization)
    u = get_user_or_404(email)
    p = get_or_create_player(email)
    return {"email": email, "profile": u["profile"], "balances": p}

@app.post("/me/progress")
def update_progress(body: ProfileProgress, authorization: Optional[str] = Header(None, alias="Authorization")):
    email = who_am_i(authorization)
    u = get_user_or_404(email)
    prof = u["profile"]
    if body.add_xp:
        prof["xp"] = max(0, prof["xp"] + body.add_xp)
    if body.add_achievements:
        # undgå dubletter
        for a in body.add_achievements:
            if a not in prof["achievements"]:
                prof["achievements"].append(a)
    if body.add_nfts:
        for n in body.add_nfts:
            if n not in prof["nfts"]:
                prof["nfts"].append(n)
    return {"msg": "progress_updated", "profile": prof}

# ====== BALANCE/PLAYER (kompatibilitet) ======
@app.get("/balance/{player_id}")
def balance(player_id: str):
    p = get_or_create_player(player_id.lower())
    return {"player_id": player_id.lower(), "locked": p["locked"], "unlocked": p["unlocked"]}

def resolve_actor(body_player_id: Optional[str], authorization: Optional[str]) -> str:
    # hvis token → brug token-identitet; ellers brug bodyens player_id (email)
    token = parse_bearer(authorization)
    if token:
        # forsøg normal access token først
        if token in sessions:
            return sessions[token]
        # forsøg remember-token som "remember:<token>"
        if token.startswith("remember:"):
            # tving klienten til at udskifte til ny access token
            return who_am_i(authorization)  # vil raise 498 med ny token
        raise HTTPException(status_code=401, detail="Invalid token")
    if body_player_id:
        return body_player_id.lower()
    raise HTTPException(status_code=401, detail="Missing auth token or player_id")

# ====== MVP CORE FLOW ======
@app.post("/f2p")
def f2p(req: F2PRequest, authorization: Optional[str] = Header(None, alias="Authorization")):
    actor = resolve_actor(req.player_id, authorization)
    p = get_or_create_player(actor)
    p["locked"] += req.reward_locked
    return {"msg": "F2P reward granted", "player": actor, "locked_added": req.reward_locked, "balances": p}

@app.post("/locked-to-unlocked")
def locked_to_unlocked(req: MatchResultRequest, authorization: Optional[str] = Header(None, alias="Authorization")):
    actor = resolve_actor(req.player_id, authorization)
    p = get_or_create_player(actor)
    if p["locked"] < req.locked_spent:
        raise HTTPException(status_code=400, detail="Not enough LOCKED to spend for this match")
    p["locked"] -= req.locked_spent
    if req.result == "win":
        p["unlocked"] += req.locked_spent
        outcome = {"converted_to_unlocked": req.locked_spent}
    else:
        outcome = {"lost_locked": req.locked_spent}
    return {"msg": "match processed", "player": actor, "result": req.result, "outcome": outcome, "balances": p}

@app.post("/withdraw")
def withdraw(req: WithdrawRequest, authorization: Optional[str] = Header(None, alias="Authorization")):
    global request_auto_id
    actor = resolve_actor(req.player_id, authorization)
    p = get_or_create_player(actor)
    if p["unlocked"] < req.amount:
        raise HTTPException(status_code=400, detail="Not enough UNLOCKED")
    p["unlocked"] -= req.amount
    wr = {
        "id": request_auto_id,
        "player_id": actor,
        "amount": req.amount,
        "address": req.address,
        "status": "pending",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "tx_hash": None,
    }
    withdraw_requests.append(wr)
    request_auto_id += 1
    return {"msg": "withdraw request created (pending admin approval)", "request": wr, "balances": p}

# ====== ADMIN ======
@app.get("/admin/pending")
def admin_pending(admin_token: str = Query(..., description="Use '?admin_token=secret123'")):
    if admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    return {"pending": [r for r in withdraw_requests if r["status"] == "pending"]}

@app.post("/admin/approve")
def admin_approve(decision: AdminDecision):
    if decision.admin_token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")
    target = next((r for r in withdraw_requests if r["id"] == decision.request_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Request not found")
    if target["status"] != "pending":
        raise HTTPException(status_code=400, detail=f"Request already {target['status']}")
    if decision.approve:
        target["status"] = "approved"
        target["tx_hash"] = f"SIMULATED_TX_{target['id']}"
        msg = "approved"
    else:
        p = get_or_create_player(target["player_id"])
        p["unlocked"] += target["amount"]
        target["status"] = "rejected"
        msg = "rejected_and_refunded"
    return {"msg": msg, "request": target}

# src/api/main.py
from fastapi import FastAPI
from .deps import init_db
from . import models
from .workers.payouts import start_worker_once

from .routers import balances, wallets, withdraw, marketplace, convert

app = FastAPI(title="Bifrost MVP")

# INIT DB (for nu; senere Alembic)
init_db(models)

# Routers
app.include_router(balances.router)
app.include_router(wallets.router)
app.include_router(withdraw.router)
app.include_router(marketplace.router)
app.include_router(convert.router)

@app.on_event("startup")
def _startup():
    start_worker_once()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/balances")
def get_balances(user_id: int):
    sql = """
    SELECT a.code, ub.amount
    FROM user_balances ub
    JOIN assets a ON a.id = ub.asset_id
    WHERE ub.user_id = :uid
    ORDER BY a.code
    """
    with engine.connect() as conn:
        rows = conn.execute(text(sql), {"uid": user_id}).mappings().all()
    return {
        "user_id": user_id,
        "db": str(engine.url),   # hjælper os at se hvilken DB den bruger
        "balances": [dict(r) for r in rows],
    }
from fastapi import Depends
from src.api.db import engine

@app.get("/debug/db")
def debug_db():
    return {"db": str(engine.url)}
