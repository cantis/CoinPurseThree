"""Tests for the character router."""
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.models import Character
from src.routers.characters import get_character


# Fixture for mock database session
@pytest.fixture()
def mock_db_session() -> MagicMock:
    """Mock database session."""
    return MagicMock(spec=Session)


# Test for get_character method
def test_get_character_success(mock_db_session) -> None:
    """Test get_character method OK."""
    # arrange
    character_id = 1
    mock_character = Character(
        character_id=1,
        character_name='Test Character',
        player_id=1,
        is_active=True,
    )
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_character

    # act
    result = get_character(character_id, mock_db_session)

    # assert
    assert result.character_id == mock_character.character_id
    assert result.character_name == mock_character.character_name
    assert result.player_id == mock_character.player_id
    assert result.is_active == mock_character.is_active


def test_get_character_not_found(mock_db_session) -> None:
    """Test get_character method not found."""
    # arrange
    character_id = 99
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # act & assert
    with pytest.raises(HTTPException) as exc_info:
        get_character(character_id, mock_db_session)

    http_not_found = 404
    assert exc_info.value.status_code == http_not_found
    assert f'Character {character_id} not found' in str(exc_info.value.detail)
