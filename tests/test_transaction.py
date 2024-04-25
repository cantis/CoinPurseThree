"""Tests for the transaction router."""
from fastapi.testclient import TestClient

from src.routers.transaction import router

# ruff: noqa: S101 ARG001 ANN001 ignore asserts, arguments unused (fixtures), missing type hint (fixtures)

client = TestClient(router)


def test_create_transaction() -> None:
    """Test create transaction."""
    # Arrange
    data = {
        'character_id': 1,
        'amount': 100.00,
        'description': 'Initial deposit',
    }

    # Act
    response = client.post(
        '/transactions/',
        json=data,
    )

    # Assert
    assert response.status_code == 201, 'Incorrect status code returned.'
    response_data = response.json()
    assert response_data['transaction_id'] is not None, 'Transaction ID not returned.'
    assert response_data['character_id'] == 1, 'Character ID not returned.'
    assert response_data['amount'] == 100.0, 'Incorrect or no amount returned.'
    assert response_data['description'] == 'Initial deposit', 'Incorrect or no description returned.'
    assert response_data['transaction_date'] is not None, 'Transaction date not returned or incorrect.'


def test_get_transactions() -> None:
    # Arrange
    # Add two transactions to the database
    transaction_data_1 = {'id': 1, 'amount': 100.0, 'description': 'Transaction 1'}
    transaction_data_2 = {'id': 2, 'amount': 200.0, 'description': 'Transaction 2'}
    client.post('/transactions', json=transaction_data_1)
    client.post('/transactions', json=transaction_data_2)

    # Act
    response = client.get('/transactions')

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    assert response.json()[0] == transaction_data_1
    assert response.json()[1] == transaction_data_2


def test_get_transaction() -> None:
    # Arrange
    transaction_data = {'id': 1, 'amount': 100.0, 'description': 'Initial deposit'}

    # Save the transaction to the database
    client.post('/transactions', json=transaction_data)

    # Act
    response = client.get(f"/transactions/{transaction_data['id']}")

    # Assert
    assert response.status_code == 200
    assert response.json() == transaction_data


def test_update_transaction() -> None:
    # Arrange
    transaction_id = 1
    updated_transaction_data = {
        'id': 1,
        'amount': 200.0,
        'description': 'Updated deposit',
    }

    # Act
    response = client.put(f'/transactions/{transaction_id}', json=updated_transaction_data)

    # Assert
    assert response.status_code == 200
    assert response.json() == updated_transaction_data


def test_delete_transaction() -> None:
    # Arrange
    transaction_data_1 = {'id': 1, 'amount': 100.0, 'description': 'Transaction 1'}
    transaction_data_2 = {'id': 2, 'amount': 200.0, 'description': 'Transaction 2'}
    client.post('/transactions', json=transaction_data_1)
    client.post('/transactions', json=transaction_data_2)

    # Act
    response = client.delete(f"/transactions/{transaction_data_2['id']}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {'detail': 'Transaction deleted'}

    # Check if the second transaction is deleted
    response = client.get(f"/transactions/{transaction_data_2['id']}")
    assert response.status_code == 404

    # Check if the first transaction still exists
    response = client.get(f"/transactions/{transaction_data_1['id']}")
    assert response.status_code == 200
    assert response.json() == transaction_data_1
