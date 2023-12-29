"""Coinpurse API."""
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
import logging

from routers import players, characters, transaction

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)
logging.debug('Coinpurse: Starting')


INSTANCE_FOLDER_PATH = '../instance'


# Create the FastAPI app and set some metadata
# See https://fastapi.tiangolo.com/tutorial/metadata/ for notes on openapi_tags (these show up in the swagger docs)
# Note: Markdown is supported in the description fields.
app = FastAPI(
    title='Coinpurse API',
    contact={
        'name': 'Evan Young',
        'email': 'cantis@gmail.com',
    },
    summary='A fantasy RPG wallet api backend.',
    description="""First attempt at a FastAPI project, a **Fantasy RPG Wallet App**, represents a characters *coinpurse* or wallet.
      Provides a record of what they get from adventuring and how they spend it.""",
    version='0.1.0',
    openapi_url='/api/v1/openapi.json',
    openapi_tags=[
        {'name': 'Test', 'description': 'Diagnostic endpoint(s).'},
        {'name': 'Players', 'description': 'Endpoints for Player Management.'},
        {'name': 'Characters', 'description': 'Endpoints for Character Management.'},
        {'name': 'Transactions', 'description': 'Endpoints for Transactions.'},
    ],
    license_info={
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT',
    },
)

# Include the routers
app.include_router(players.router)
app.include_router(characters.router)
app.include_router(transaction.router)


@app.get('/', tags=['Healthcheck'])
async def root():
    logging.debug('root endpoint')
    """Root endpoint for the API."""
    return {'message': 'Coinpurse is UP!'}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    self, request: Request, exc: RequestValidationError
) -> JSONResponse:
    logging.debug('validation_exception_handler')
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    # self.logger.error(f'{request}: {exc_str}')
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
