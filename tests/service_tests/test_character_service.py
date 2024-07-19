"""Character Service, crud methods for character model."""
from typing import Optional

from sqlmodel import Session, select

from src.models import Character


class CharacterNotFoundError(Exception):
    """Character not found error."""

    def __init__(self, character_id: int) -> None:
        """Initialize the error."""
        self.message = f'Character with id {character_id} not found.'
        self.character_id = character_id


class CharacterService:
    """Character Service, crud methods for character model."""

    @staticmethod
    def create(session: Session, name: str) -> Character:
        """Create a character."""
        character = Character(name=name)
        session.add(character)
        session.commit()
        session.refresh(character)
        return character
