from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import APIRouter

router = APIRouter()


class Player(BaseModel):
    userId: int
    playerName: str
    password: str
    email: EmailStr
    isAdmin: Optional[bool] = False


# In-memory storage for players
players = {}


@router.post('/players/', tags=['Players'])
async def create_player(player: Player):
    players[player.userId] = player
    return {'message': 'Player created'}


@router.get('/players/{user_id}', tags=['Players'])
async def read_player(user_id: int):
    player = players.get(user_id)
    if not player:
        return {'message': 'Player not found'}
    return player


@router.put('/players/{user_id}', tags=['Players'])
async def update_player(user_id: int, player: Player):
    if user_id not in players:
        return {'message': 'Player not found'}
    players[user_id] = player
    return {'message': 'Player updated'}


@router.delete('/players/{user_id}', tags=['Players'])
async def delete_player(user_id: int):
    if user_id not in players:
        return {'message': 'Player not found'}
    del players[user_id]
    return {'message': 'Player deleted'}


@router.get('/players/', tags=['Players'])
async def get_all_players():
    return list(players.values())
