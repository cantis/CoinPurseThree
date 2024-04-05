from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import logging
from typing import Optional
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from src.database.models import get_db, DbCharacter

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


@router.get(
    '/characters/{character_id}',
    tags=['Characters'],
    status_code=200,
    response_model=Character,
    responses={404: {'description': 'Character \<id\> not found'}},
)
async def get_character(character_id: int, db: Session = Depends(get_db)) -> Character:
    """Get a character by ID."""
    logging.debug(f'Get Character: {character_id}')
    db_character = (
        db.query(DbCharacter).filter(DbCharacter.characterId == character_id).first()
    )
    if db_character is None:
        raise HTTPException(
            status_code=404, detail=f'Character {character_id} not found'
        )
    character = Character(
        characterId=db_character.characterId,
        characterName=db_character.characterName,
        playerId=db_character.playerId,
        isActive=db_character.isActive,
    )
    return character


@router.post(
    '/characters', tags=['Characters'], status_code=201, response_model=Character
)
async def create_character(
    character: CreateCharacter, db: Session = Depends(get_db)
) -> Character:
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


@router.put(
    '/characters/{character_id}',
    tags=['Characters'],
    status_code=200,
    response_model=Character,
    responses={404: {'description': 'Character \<id\> not found'}},
)
async def update_character(
    character_id: int, updated_character: UpdateCharacter, db: Session = Depends(get_db)
) -> Character:
    try:
        logging.debug(f'Update Character: {character_id} {updated_character}')
        db_character = (
            db.query(DbCharacter)
            .filter(DbCharacter.characterId == character_id)
            .first()
        )
        if db_character is None:
            raise HTTPException(status_code=404, detail='Character not found')
        db_character.characterName = (
            updated_character.characterName
            if updated_character.characterName
            else db_character.characterName
        )
        db_character.playerId = (
            updated_character.playerId
            if updated_character.playerId
            else db_character.playerId
        )
        db_character.isActive = (
            updated_character.isActive
            if updated_character.isActive
            else db_character.isActive
        )
        db.commit()
        db.refresh(db_character)
        updated_character = Character(
            characterId=db_character.characterId,
            characterName=db_character.characterName,
            playerId=db_character.playerId,
            isActive=db_character.isActive,
        )
    except Exception as e:
        logging.error(f'Error updating character: {e}')
        raise HTTPException(
            status_code=500, detail='Internal server error updating character.'
        ) from e
    return updated_character


@router.delete(
    '/characters/{character_id}',
    tags=['Characters'],
    status_code=204,
    responses={404: {'description': 'Character \<id\> not found'}},
)
async def delete_character(character_id: int, db: Session = Depends(get_db)) -> None:
    logging.debug(f'Delete Character: {character_id}')
    db_character = (
        db.query(DbCharacter).filter(DbCharacter.characterId == character_id).first()
    )
    if db_character is None:
        raise HTTPException(
            status_code=404, detail=f'Character {character_id} not found'
        )
    db.delete(db_character)
    return


@router.get(
    '/characters', tags=['Characters'], status_code=200, response_model=list[Character]
)
async def get_all_characters(db: Session = Depends(get_db)) -> list[Character]:
    logging.debug('Get All Characters')
    db_characters = db.query(DbCharacter).all()
    characters = []
    for db_character in db_characters:
        character = Character(
            characterId=db_character.characterId,
            characterName=db_character.characterName,
            playerId=db_character.playerId,
            isActive=db_character.isActive,
        )
        characters.append(character)
    return characters
