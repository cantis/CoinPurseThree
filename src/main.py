"""Coinpurse API."""
import logging

from database.models import create_db_and_tables
from dotenv import load_dotenv
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from routers import characters, players, transaction

# Load environment variables from .env file
load_dotenv('.env')

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)
logging.debug('Coinpurse: Starting')


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

    # Create the database and tables if necessary
    create_db_and_tables()

    # Include the routers, add additional routers here as needed
    app.include_router(players.router)
    app.include_router(characters.router)
    app.include_router(transaction.router)
    return app


# Create the FastAPI app and set some metadata
# See https://fastapi.tiangolo.com/tutorial/metadata/ for notes on openapi_tags (these show up in the swagger docs)
# Note: Markdown is supported in the description fields.
app = create_app()


# Root endpoint for the API
@app.get('/', tags=['Healthcheck'], status_code=200, summary='Check if Coinpurse is up.')
async def root() -> None:
    """Root endpoint for the API."""
    logging.debug('root endpoint hit')
    return {'message': 'Coinpurse is UP!'}


# Handle validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Handle validation errors."""
    logging.exception('validation_exception_handler')
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    content = {'status_code': 10422, 'message': exc_str, 'data': request.url}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


# Handle general exceptions
@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle general exceptions."""
    logging.exception('general_exception_handler')
    content = {'status_code': 500, 'message': 'Internal Server Error', 'data': request.url}
    return JSONResponse(
        content=content,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
