from tests.conftest import client
from database.models import DbCharacter as Character

def add_player_to_db(db: Session = Depends(get_db)):
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
    }





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
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
        'isActive': True
    }
    client.post(
        '/players/',
        json=data,
    )
    data = {
        'characterName': 'Test Character',
        'playerId': 1,
        'isActive': True
    }

    # Act
    response = client.post('/characters/', json=data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['characterId'] == 1
    assert data['characterName'] == 'Test Character'
    assert data['playerId'] == 1
    assert data['isActive'] is True



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
