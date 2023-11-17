"""Coinpurse API."""
import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

DATABASE_URL = 'sqlite:///../instance/coin_purse.db'

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    """Get a database session."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.on_event('startup')
async def startup():
    """Create the database tables, if they don't already exist."""
    if not os.path.exists(DATABASE_URL):
        Base.metadata.create_all(bind=engine)


@app.get('/')
async def root():
    """Root endpoint for the API."""
    return {'message': 'Coinpurse is UP!'}
