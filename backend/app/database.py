from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# DATABASE_URL = "sqlite:///./projectDatabase.db"
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# pool_pre_ping checks a connection is alive before using it, so requests after
# Neon's idle auto-suspend transparently reconnect instead of erroring.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from app import models
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
