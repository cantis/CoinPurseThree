from fastapi.params import Depends
from tests.conftest import client
from database.models import DbCharacter as Character
import pytest
from sqlalchemy.orm.session import Session

from database.models import get_db

# @pytest.fixture(scope='module')
# def add_player_to_db(db: Session = Depends(get_db)):
#     data = {
#         'playerName': 'test_player',
#         'password': 'test_password',
#         'email': 'test@noplace.com',
#         'isAdmin': False,
#     }
#     client.post(
#         '/players/',
#         json=data,
#     )

def test_get_characters():
    # Arrange
    response_data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
        'isActive': True
    }
    client.post(
        '/players/',
        json=response_data,
    )
    character1 = {
        'characterName': 'Character 1',
        'playerId': 1,
        'isActive': True
    }
    client.post('/characters/', json=character1)
    character2 = {
        'characterName': 'Character 2',
        'playerId': 1,
        'isActive': True
    }
    client.post('/characters/', json=character2)

    # Act
    response = client.get('/characters')

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['characterName'] == 'Character 1'
    assert response_data[1]['characterName'] == 'Character 2'


def test_create_character():
    # Arrange
    test_player = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
        'isActive': True
    }
    client.post(
        '/players/',
        json=test_player,
    )

    character_to_add = {
        'characterName': 'Test Character',
        'playerId': 1,
        'isActive': True
    }

    # Act
    response = client.post('/characters/', json=character_to_add)

    # Assert
    assert response.status_code == 201
    character_to_add = response.json()
    assert character_to_add['characterId'] == 1
    assert character_to_add['characterName'] == 'Test Character'
    assert character_to_add['playerId'] == 1
    assert character_to_add['isActive'] is True



def test_update_character():
    # Arrange
    response_data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
        'isActive': True
    }
    client.post(
        '/players/',
        json=response_data,
    )
    response_data = {
        'characterName': 'Test Character',
        'playerId': 1,
        'isActive': False
    }
    client.post('/characters/', json=response_data)

    # Act
    new_data = {
        'characterName': 'Adam Alpha',
        'playerId': 1,
        'isActive': False
    }
    response = client.put('/characters/1', json=new_data)

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['characterName'] == 'Adam Alpha'
    assert response_data['playerId'] == 1
    assert response_data['isActive'] is False


def test_delete_character():
    # Arrange: No arrangement necessary for this test
    response_data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
        'isActive': True
    }
    client.post(
        '/players/',
        json=response_data,
    )
    response_data = {
        'characterName': 'Test Character',
        'playerId': 1,
        'isActive': False
    }
    client.post('/characters/', json=response_data)

    # Act
    response = client.delete('/characters/1')

    # Assert
    assert response.status_code == 204
