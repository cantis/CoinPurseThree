"""Healthcheck router for the API."""
import logging

from fastapi import APIRouter

router = APIRouter()


# Root endpoint for the API
@router.get('/', tags=['Healthcheck'], status_code=200, summary='Base endpoint for the API.')
async def root() -> None:
    """Root endpoint for the API."""
    logging.debug('root endpoint hit')
    return {'message': 'Coinpurse is UP!'}
