"""Coinpurse API."""
import logging

from database.models import create_db_and_tables
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routers import characters, home, players, transaction

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)
logging.debug('Coinpurse: Starting')


INSTANCE_FOLDER_PATH = '../instance'


# application factory pattern
def create_app() -> FastAPI:
    """Create the FastAPI app."""
    app = FastAPI(
        title='Coinpurse API',
        contact={
            'name': 'Evan Young',
            'email': 'cantis@gmail.com',
        },
        summary='A fantasy RPG wallet api backend.',
        description="""First attempt at a FastAPI project, a **Fantasy RPG Wallet App**, represents a characters *coinpurse*
        or wallet. Provides a record of what they get from adventuring and how they spend it.""",
        version='0.1.0',
        openapi_url='/api/v1/openapi.json',
        openapi_tags=[
            {'name': 'Players', 'description': 'Endpoints for Player Management.'},
            {'name': 'Characters', 'description': 'Endpoints for Character Management.'},
            {'name': 'Transactions', 'description': 'Endpoints for Transactions.'},
            {'name': 'Test', 'description': 'Diagnostic endpoint(s).'},
            {'name': 'Healthcheck', 'description': 'Healthcheck endpoint.'},
        ],
        license_info={
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT',
        },
    )

    # Create the database and tables
    create_db_and_tables()

    # Include the routers, add additional routers here as needed
    app.include_router(home.router)
    app.include_router(players.router)
    app.include_router(characters.router)
    app.include_router(transaction.router)
    return app


# Create the FastAPI app and set some metadata
# See https://fastapi.tiangolo.com/tutorial/metadata/ for notes on openapi_tags (these show up in the swagger docs)
# Note: Markdown is supported in the description fields.
app = create_app()
