"""Test the main module."""

from fastapi import status

from tests.conftest import test_client


def test_read_main() -> None:
    """Test read main."""
    # Arrange

    # Act
    response = test_client.get('/')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Coinpurse is UP!'}
