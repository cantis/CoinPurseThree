"""Coinpurse API."""
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routers import players, characters, transaction

INSTANCE_FOLDER_PATH = '../instance'
# DATABASE_URL = 'sqlite:///../instance/coin_purse.db'
DATABASE_URL = 'sqlite:///coin_purse.db'

sesh = sessionmaker(bind=create_engine(DATABASE_URL))

app = FastAPI()

app.include_router(players.router)
app.include_router(characters.router)
app.include_router(transaction.router)


# Dependency to get the database session
def get_db() -> None:
    """Get a database session."""
    database = sesh()
    try:
        yield database
    finally:
        database.close()


@app.get('/', tags=["Test"])
async def root() -> dict:
    """Root endpoint for the API."""
    return {'message': 'Coinpurse is UP!'}
