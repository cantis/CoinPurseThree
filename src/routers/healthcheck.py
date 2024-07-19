"""Healthcheck router for the API."""
import logging

from fastapi import APIRouter, HTTPException

from src.models import TestItem

router = APIRouter()


# Root endpoint for the API
@router.get('/', tags=['Healthcheck'], status_code=200, summary='Base endpoint for the API.')
async def root() -> None:
    """Root endpoint for the API."""
    logging.debug('root endpoint hit')
    return {'message': 'Coinpurse is UP!'}


# Endpoints for testing validation
@router.post('/test-validation')
async def test_validation(item: TestItem) -> dict:
    """Endpoint for testing validation."""
    # Since this is for demonstration, we're not doing any processing with `item`.
    # In a real scenario, you would handle the validated data here.
    return {'message': 'Data validated successfully'}


@router.get('/test-exception')
async def test_exception() -> None:
    """Endpoint for testing the general exception handler."""
    raise HTTPException(status_code=500, detail='Internal Server Error')
