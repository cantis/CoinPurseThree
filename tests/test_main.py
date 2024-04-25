"""Test the main module."""
import html

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
    assert response.status_code == html.HTTPStatus.OK.value
    assert response.json() == {'message': 'Coinpurse is UP!'}
