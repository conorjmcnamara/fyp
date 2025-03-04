import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as db:
        yield db
