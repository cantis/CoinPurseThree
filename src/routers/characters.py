from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class Character(BaseModel):
    """Represents a character in the game, belonging to a player."""

    characterId: int
    playerId: int
    name: str


characters = {}


@router.get('/characters/{character_id}', tags=['Characters'])
async def get_character(character_id: int):
    for character in characters:
        if character['id'] == character_id:
            return character
    return {'message': 'Character not found'}


@router.post('/characters', tags=['Characters'])
async def create_character(character: Character):
    characters.append(character)
    return {'message': 'Character created successfully'}


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
