"""Character routes."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from database.models import Character, CharacterBase
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel

# if TYPE_CHECKING:
#     from sqlalchemy.orm.session import Session

router = APIRouter()

# # region Pydantic Models




# class UpdateCharacter(BaseModel):
#     """Update a character."""

#     character_name: str | None
#     player_id: int | None
#     is_active: bool | None


# # endregion


# @router.get(
#     '/characters/{character_id}',
#     tags=['Characters'],
#     status_code=200,
#     response_model=Character,
#     responses={404: {'description': 'Character \<id\> not found'}},
# )
# async def get_character(character_id: int, db: Session = Depends(get_db)) -> Character:
#     """Get a character by ID."""
#     logging.debug('Getting Character', extra={'character_id': character_id})
#     db_character = db.query(DbCharacter).filter(DbCharacter.characterId == character_id).first()
#     if db_character is None:
#         raise HTTPException(status_code=404, detail=f'Character {character_id} not found')
#     return Character(
#         character_id=db_character.characterId,
#         character_name=db_character.characterName,
#         player_id=db_character.playerId,
#         is_active=db_character.isActive,
#     )


# @router.post(
#     '/characters',
#     tags=['Characters'],
#     status_code=201,
#     response_model=Character,
# )
# async def create_character(character: CreateCharacter, db: Session = Depends(get_db)) -> Character:
#     """Create a character."""
#     logging.debug('Create Character:', extra={'character': character})
#     character_to_add = DbCharacter(
#         characterName=character.character_name,
#         playerId=character.player_id,
#         isActive=character.is_active,
#     )
#     db.add(character_to_add)
#     db.commit()
#     db.refresh(character_to_add)
#     return character_to_add


# @router.put(
#     '/characters/{character_id}',
#     tags=['Characters'],
#     status_code=200,
#     response_model=Character,
#     responses={404: {'description': 'Character \<id\> not found'}},
# )
# async def update_character(
#     character_id: int, updated_character: UpdateCharacter, db: Session = Depends(get_db)
# ) -> Character:
#     """Update a character."""
#     try:
#         logging.debug('Update Character:', extra={'character_id': character_id, 'updated_character': updated_character})
#         db_character = db.query(DbCharacter).filter(DbCharacter.characterId == character_id).first()
#         if db_character is None:
#             raise HTTPException(status_code=404, detail='Character not found')
#         db_character.characterName = (
#             updated_character.character_name if updated_character.character_name else db_character.characterName
#         )
#         db_character.playerId = updated_character.player_id if updated_character.player_id else db_character.playerId
#         db_character.isActive = updated_character.is_active if updated_character.is_active else db_character.isActive
#         db.commit()
#         db.refresh(db_character)
#         updated_character = Character(
#             character_id=db_character.characterId,
#             character_name=db_character.characterName,
#             player_id=db_character.playerId,
#             is_active=db_character.isActive,
#         )
#     except Exception as e:
#         logging.error(f'Error updating character: {e}')
#         raise HTTPException(status_code=500, detail='Internal server error updating character.') from e
#     return updated_character


# @router.delete(
#     '/characters/{character_id}',
#     tags=['Characters'],
#     status_code=204,
#     responses={404: {'description': 'Character \<id\> not found'}},
# )
# async def delete_character(character_id: int, db: Session = Depends(get_db)) -> None:
#     """Delete a character by ID."""
#     logging.debug('Delete Character', extra={'character_id': character_id})
#     db_character = db.query(DbCharacter).filter(DbCharacter.characterId == character_id).first()
#     if db_character is None:
#         raise HTTPException(status_code=404, detail=f'Character {character_id} not found')
#     db.delete(db_character)


# @router.get('/characters', tags=['Characters'], status_code=200, response_model=list[Character])
# async def get_all_characters(db: Session = Depends(get_db)) -> list[Character]:
#     """Get all characters."""
#     logging.debug('Get All Characters')
#     db_characters = db.query(DbCharacter).all()
#     characters = []
#     for db_character in db_characters:
#         character = Character(
#             character_id=db_character.characterId,
#             character_name=db_character.characterName,
#             player_id=db_character.playerId,
#             is_active=db_character.isActive,
#         )
#         characters.append(character)
#     return characters
