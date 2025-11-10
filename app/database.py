# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------- 1. Build a safe, relative path ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR   = os.path.join(BASE_DIR, "data")
DB_PATH  = os.path.join(DB_DIR, "addresses.db")

os.makedirs(DB_DIR, exist_ok=True)          
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(f"\nSQLite DB path: {DB_PATH}\n")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()