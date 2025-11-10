# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------- 1. Build a safe, relative path ----------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR   = os.path.join(BASE_DIR, "data")
DB_PATH  = os.path.join(DB_DIR, "addresses.db")

os.makedirs(DB_DIR, exist_ok=True)          # <-- creates folder if missing
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Debug print (you will see this in the terminal)
print(f"\nSQLite DB path: {DB_PATH}\n")

# ---------- 2. Engine ----------
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    # echo=True   # uncomment only for debugging SQL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()