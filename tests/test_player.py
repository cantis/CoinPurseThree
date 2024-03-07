from tests.conftest import client


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
