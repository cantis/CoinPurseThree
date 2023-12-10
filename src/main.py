"""Coinpurse API."""
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from routers import players, characters, transaction

INSTANCE_FOLDER_PATH = '../instance'
# DATABASE_URL = 'sqlite:///../instance/coin_purse.db'
DATABASE_URL = 'sqlite:///coin_purse.db'

sesh = sessionmaker(bind=create_engine(DATABASE_URL))

app = FastAPI(
    title="Coinpurse API",
    description="API for Coinpurse, a fantasy RPG wallet app.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json",
    openapi_tags=[{
        "name": "Test",
        "description": "Diagnostic endpoint(s)."
    }, {
        "name": "Players",
        "description": "Endpoints for Player Management."
    }, {
        "name": "Characters",
        "description": "Endpoints for Character Management."
    }, {
        "name": "Transactions",
        "description": "Endpoints for Transactions."
    }]
)

    # docs_url="/",
    # redoc_url=None,
    # openapi_tags=[{
    #     "name": "Test",
    #     "description": "Test endpoints."
    # }, {
    #     "name": "Players",
    #     "description": "Endpoints for the Player resource."
    # }, {
    #     "name": "Characters",
    #     "description": "Endpoints for the Character resource."
    # }, {
    #     "name": "Transactions",
    #     "description": "Endpoints for the Transaction resource."
    # }]


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
