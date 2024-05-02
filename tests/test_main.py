"""Test the main module."""
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app

# ruff: noqa: S101 ARG001 ANN001 ignore asserts, arguments unused (fixtures), missing type hint (fixtures)

client = TestClient(app)


def test_read_main() -> None:
    """Test read main."""
    # Arrange

    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Coinpurse is UP!'}
