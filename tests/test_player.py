from tests.conftest import client

def test_create_player_ok() -> None:
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


def test_get_player_ok(add_test_player) -> None:
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

def test_update_player_ok(add_test_player) -> None:
    # arrange

    # act
    data_to_update = {
        'playerId': 1,
        'playerName': 'updated_player',
        'password': 'updated_password',
        'email': 'updated@noplace.com',
        'isAdmin': True,
        'isActive': False,
    }

    response = client.put(
        '/players/1',
        json=data_to_update,
    )

    # assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['playerId'] == data_to_update['playerId']
    assert response_data['playerName'] == data_to_update['playerName']
    assert response_data['password'] == data_to_update['password']
    assert response_data['email'] == data_to_update['email']
    assert response_data['isAdmin'] is data_to_update['isAdmin']

def test_delete_player_ok() -> None:
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

def test_get_all_players_ok(add_test_player) -> None:
    # arrange
    # act
    response = client.get('/players')
    # assert
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0

def test_get_player_error() -> None:
    # arrange

    # act
    response = client.get('/players/999')

    # assert
    assert response.status_code == 404
    response_data = response.json()
    assert response_data['detail'] == 'Player 999 not found'
