from fastapi import APIRouter
from fastapi.params import Depends
import logging
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from database.models import get_db, DbCharacter

router = APIRouter()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)

# region Pydantic Models

class Character(BaseModel):
    """Represents a character."""
    characterId: int
    characterName: str
    playerId: int
    isActive: bool

class CreateCharacter(BaseModel):
    """Create a character."""
    characterName: str
    playerId: int
    isActive: bool

class UpdateCharacter(BaseModel):
    """Update a character."""
    characterName: Optional[str]
    playerId: Optional[int]
    isActive: Optional[bool]

# endregion

@router.get('/characters/{character_id}', tags=['Characters'])
async def get_character(character_id: int):
    for character in characters:
        if character['id'] == character_id:
            return character
    return {'message': 'Character not found'}


@router.post('/characters', tags=['Characters'], status_code=201, response_model=Character)
async def create_character(character: CreateCharacter, db: Session = Depends(get_db)) -> Character:
    logging.debug(f'Create Character: {character}')
    dbCharacterToAdd = DbCharacter(
        characterName=character.characterName,
        playerId=character.playerId,
        isActive=character.isActive,
    )
    db.add(dbCharacterToAdd)
    db.commit()
    db.refresh(dbCharacterToAdd)
    return dbCharacterToAdd


@router.put('/characters/{character_id}', tags=['Characters'])
async def update_character(character_id: int, updated_character: Character):
    for character in characters:
        if character['id'] == character_id:
            character.update(updated_character)
            return {'message': 'Character updated successfully'}
    return {'message': 'Character not found'}


@router.delete('/characters/{character_id}', tags=['Characters'])
async def delete_character(character_id: int):
    for character in characters:
        if character['id'] == character_id:
            characters.remove(character)
            return {'message': 'Character deleted successfully'}
    return {'message': 'Character not found'}


@router.get('/characters', tags=['Characters'])
async def get_all_characters():
    return list(characters.values())
