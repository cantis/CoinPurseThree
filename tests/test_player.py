from tests.conftest import client, override_get_db
from database.models import DbPlayer as Player


def test_create_player() -> None:
    # arrange
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
    }

    # act
    response = client.post(
        '/players/',
        json=data,
    )

    # assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'
    assert response_data['email'] == 'test@noplace.com'
    assert response_data['isAdmin'] is False


def test_get_player() -> None:
    # arrange

    # act
    response = client.get('/players/1')

    # assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'
    assert response_data['email'] == 'test@noplace.com'
    assert response_data['isAdmin'] is False

def test_update_player() -> None:
    # arrange
    # add a player to the database to start
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
    }
    client.post(
        '/players/',
        json=data,
    )

    # act
    # update the player
    data = {
        'playerName': 'updated_player',
        'password': 'updated_password',
        'email': 'updated@noplace.com',
        'isAdmin': True,
        'isActive': False,
    }

    response = client.put(
        '/players/1',
        json=data,
    )

    # assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'updated_player'
    assert response_data['password'] == 'updated_password'
    assert response_data['email'] == 'updated@noplace.com'
    assert response_data['isAdmin'] is True

def test_delete_player() -> None:
    # arrange
    # add a player to the database to start
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
    }
    client.post(
        '/players/',
        json=data,
    )

    # act
    response = client.delete('/players/1')

    # assert
    assert response.status_code == 204

def test_get_all_players() -> None:
    # arrange
    # act
    response = client.get('/players')
    # assert
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0

def test_get_invalid_player_id() -> None:
    # arrange
    # act
    response = client.get('/players/999')
    # assert
    assert response.status_code == 404
