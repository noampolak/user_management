# app/database.py
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Example: postgresql://user:password@host:port/dbname
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/mydatabase"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
