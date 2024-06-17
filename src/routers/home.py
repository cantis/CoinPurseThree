"""Base router for the API."""
# Includes the root endpoint and exception handler for validation errors.

import logging

from fastapi import APIRouter, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get('/', tags=['Healthcheck'], status_code=200, summary='Check if Coinpurse is up.')
async def root() -> None:
    """Root endpoint for the API."""
    logging.debug('root endpoint hit')
    return {'message': 'Coinpurse is UP!'}


@router.exception_handler(RequestValidationError)
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
