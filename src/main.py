"""Coinpurse API."""
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routers import players

INSTANCE_FOLDER_PATH = '../instance'
# DATABASE_URL = 'sqlite:///../instance/coin_purse.db'
DATABASE_URL = 'sqlite:///coin_purse.db'

sesh = sessionmaker(bind=create_engine(DATABASE_URL))

app = FastAPI()

app.include_router(players.router)

# Dependency to get the database session
def get_db() -> None:
    """Get a database session."""
    database = sesh()
    try:
        yield database
    finally:
        database.close()


@app.get('/')
async def root() -> dict:
    """Root endpoint for the API."""
    return {'message': 'Coinpurse is UP!'}
