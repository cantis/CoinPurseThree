"""Coinpurse API."""
from contextlib import asynccontextmanager
import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

INSTANCE_FOLDER_PATH = "../instance"
DATABASE_URL = "sqlite:///../instance/coin_purse.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.on_event("startup")
async def startup():
    # Create the instance folder if it doesn't exist
    if not os.path.exists(INSTANCE_FOLDER_PATH):
        os.makedirs(INSTANCE_FOLDER_PATH)
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint for the API."""
    return {"message": "Coinpurse is UP!"}
