"""Coinpurse API."""
import os
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base

INSTANCE_FOLDER_PATH = '../instance'
# DATABASE_URL = 'sqlite:///../instance/coin_purse.db'
DATABASE_URL = 'sqlite:///coin_purse.db'

sesh = sessionmaker(bind=create_engine(DATABASE_URL))

app = FastAPI()


# Dependency to get the database session
def get_db() -> None:
    """Get a database session."""
    database = sesh()
    try:
        yield database
    finally:
        database.close()


@app.on_event('startup')
async def startup() -> None:
    # Create the instance folder if it doesn't exist
    if not os.path.exists(INSTANCE_FOLDER_PATH):
        os.makedirs(INSTANCE_FOLDER_PATH)
    sesh = sessionmaker(bind=create_engine(DATABASE_URL))
    with sesh() as db:
        db.commit()


@app.get('/')
async def root() -> dict:
    """Root endpoint for the API."""
    return {'message': 'Coinpurse is UP!'}
