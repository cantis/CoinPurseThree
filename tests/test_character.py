from tests.conftest import client
from database.models import DbCharacter as Character


def test_get_characters():
    # Arrange:
    # Arrange
    character1 = Character(name='Character 1', level=1)
    character2 = Character(name='Character 2', level=2)
    character1.save()
    character2.save()

    # Act
    response = client.get('/characters')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]['name'] == character1.name
    assert data[0]['level'] == character1.level
    assert data[1]['name'] == character2.name
    assert data[1]['level'] == character2.level


def test_create_character():
    # Arrange
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
        'isActive': True
    }
    playerAdded = client.post(
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
    new_data = {'name': 'Updated Name', 'level': 2}

    # Act
    response = client.put(f'/characters/{test_character.id}', json=new_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == new_data['name']
    assert data['level'] == new_data['level']


def test_delete_character():
    # Arrange: No arrangement necessary for this test

    # Act
    response = client.delete(f'/characters/{test_character.id}')

    # Assert
    assert response.status_code == 204
