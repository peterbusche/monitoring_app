# db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into environment

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "5432")
database = os.getenv("DB_NAME", "monitoring_app_db")

DB_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
