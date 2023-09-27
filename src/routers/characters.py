import fastapi
from fastapi import Path
from pydantic import BaseModel

router = fastapi.APIRouter()


class Character(BaseModel):
    charcter_name: str
    player_id: int
    is_active: bool


characters = []


@router.get('/character/', response_model=list[Character])
async def list_characters():
    '''Get a list of characters'''
    return characters


@router.get('/character/{id}', response_model=Character)
async def get_character_by_id(id: int):
    '''Get a character by id'''
    return {'Character Id': id}


@router.post('/character/')
async def create_character(character: Character):
    '''Add a new character'''
    characters.append(character)


@router.put('/character/')
async def update_character(character: Character):
    '''Update a character'''
    return {'Character Name:': character.charcter_name}


@router.delete('/character/{id}')
async def delete_character(id: int):
    '''Delete a character'''
    return {'Character Id': id}
