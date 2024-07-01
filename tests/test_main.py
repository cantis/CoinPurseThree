"""Test the main module."""

from fastapi import status

from tests.conftest import test_client


def test_root_endpoint() -> None:
    """Test the root endpoint."""
    # arrange, act
    response = test_client.get('/')

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Coinpurse is UP!'}

def test_validation_error_handler() -> None:
    """Test the validation error handler."""
    # arrange
    # This assumes an endpoint '/test-validation' exists for demonstration purposes
    invalid_data = {'invalid': 'data'}

    # act
    response = test_client.post('/test-validation', json=invalid_data)

    # assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert 'detail' in response.text

def test_general_exception_handler() -> None:
    """Test the general exception handler."""
    # arrange, act
    # This assumes an endpoint '/test-exception' exists for demonstration purposes
    response = test_client.get('/test-exception')

    # assert
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert 'Internal Server Error' in response.text
