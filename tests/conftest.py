"""Configuration for the test suite."""
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.routers import healthcheck


def create_test_client() -> 'FastAPI':
    """Create a FastAPI app for testing."""
    app = FastAPI()

    # app.include_router(players.router)
    #app.include_router(characters.router)
    # app.include_router(transaction.router)
    app.include_router(healthcheck.router)
    return TestClient(app)


test_client = create_test_client()
