from sqlalchemy import create_engine, text
import os

# Hent DB-url fra .env eller brug default sqlite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bifrost.db")

# Lav engine (connection til DB)
engine = create_engine(DATABASE_URL, future=True)
