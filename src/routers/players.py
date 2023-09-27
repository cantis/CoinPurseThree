import fastapi
from fastapi import Path
from pydantic import BaseModel

router = fastapi.APIRouter()


class Player(BaseModel):
    name: str
    email: str
    is_active: bool


players = []


@router.get('/player/', response_model=list[Player])
async def list_players():
    '''Get a list of players'''
    return players


@router.get('/player/{id}', response_model=Player)
async def get_player_by_id(
    id: int = Path(..., description='The id of the player to get')
):
    '''Get a player by id'''
    return players[id]


@router.post('/player/')
async def create_player(player: Player):
    '''Add a new player'''
    players.append(player)
    return {'Player Name:': player.name}


@router.put('/player/')
async def update_player(player: Player):
    '''Update a player'''
    return {'Player Name:': player.name}


@router.delete('/player/{id}')
async def delete_player(id: int):
    '''Delete a player'''
    return {'Player Id': id}
