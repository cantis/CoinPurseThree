from tests.conftest import client


def test_get_characters_ok(add_test_characters):
    # Arrange

    # Act
    response = client.get('/characters')

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) > 0
    assert response_data[0]['characterName'] == 'Character 1'
    assert response_data[1]['characterName'] == 'Character 2'


def test_create_character_ok(add_test_player):
    # Arrange
    data = {'characterName': 'Test Character', 'playerId': 1, 'isActive': True}

    # Act
    response = client.post('/characters/', json=data)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['characterId'] == data['characterId']
    assert data['characterName'] == data['characterName']
    assert data['playerId'] == data['playerId']
    assert data['isActive'] is data['isActive']


def test_update_character_ok(add_test_player):
    # Arrange
    response_data = {
        'characterName': 'Test Character',
        'playerId': 1,
        'isActive': False,
    }
    client.post('/characters/', json=response_data)

    # Act
    new_data = {'characterName': 'Adam Alpha', 'playerId': 1, 'isActive': False}
    response = client.put('/characters/1', json=new_data)

    # Assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['characterName'] == 'Adam Alpha'
    assert response_data['playerId'] == 1
    assert response_data['isActive'] is False


def test_delete_character(add_test_player):
    # Arrange:
    response_data = {
        'characterName': 'Test Character',
        'playerId': 1,
        'isActive': False,
    }
    client.post('/characters/', json=response_data)

    # Act
    response = client.delete('/characters/1')

    # Assert
    assert response.status_code == 204



def test_get_character_by_id_error(add_test_characters):
    # Arrange

    # Act
    response = client.get('/characters/999')

    # Assert
    assert response.status_code == 404
    response_data = response.json()
    assert response_data['detail'] == 'Character 999 not found'
