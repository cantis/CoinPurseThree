"""Tests for the player module."""
import html

from tests.conftest import client

# ruff: noqa: S101 ARG001 ANN001 ignore asserts, arguments unused (fixtures), missing type hint (fixtures)


def test_create_player_ok() -> None:
    """Test create player."""
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
    assert response.status_code == html.HTTPStatus.CREATED.value
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'  # noqa: S105
    assert response_data['email'] == 'test@noplace.com'
    assert response_data['isAdmin'] is False


def test_get_player_ok(_add_test_player) -> None:
    """Test get player."""
    # arrange

    # act
    response = client.get('/players/1')

    # assert
    assert response.status_code == html.HTTPStatus.OK.value
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'  # noqa: S105
    assert response_data['email'] == 'test@noplace.com'
    assert response_data['isAdmin'] is False


def test_update_player_ok(_add_test_player) -> None:
    """Test update player."""
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
    assert response.status_code == html.HTTPStatus.OK.value
    response_data = response.json()
    assert response_data['playerId'] == data_to_update['playerId']
    assert response_data['playerName'] == data_to_update['playerName']
    assert response_data['password'] == data_to_update['password']
    assert response_data['email'] == data_to_update['email']
    assert response_data['isAdmin'] is data_to_update['isAdmin']


def test_delete_player_ok() -> None:
    """Test delete player."""
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
    assert response.status_code == html.httpstatus.NO_CONTENT.value


def test_get_all_players_ok(_add_test_player) -> None:
    """Test get all players."""
    # arrange

    # act
    response = client.get('/players')

    # assert
    assert response.status_code == html.HTTPStatus.OK.value
    response_data = response.json()
    assert len(response_data) > 0


def test_get_player_error() -> None:
    """Test get player error."""
    # arrange

    # act
    response = client.get('/players/999')

    # assert
    assert response.status_code == html.HTTPStatus.NOT_FOUND.value
    response_data = response.json()
    assert response_data['detail'] == 'Player 999 not found'
