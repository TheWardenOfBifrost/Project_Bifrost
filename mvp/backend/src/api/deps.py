# src/api/deps.py
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bifrost.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})

def init_db(models_module):
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

# Dummy current_user dep (replace with your auth)
from pydantic import BaseModel
class User(BaseModel):
    id: int
    is_admin: bool = False

def get_current_user() -> User:
    # TODO: wire to your JWT auth; for now user 1
    return User(id=1, is_admin=True)
