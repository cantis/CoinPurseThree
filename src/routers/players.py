from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm.session import Session

from database.models import get_db, DbPlayer

router = APIRouter()


class Player(BaseModel):
    """Represents a player in the game."""

    userId: int
    playerName: str
    password: str
    email: EmailStr
    isAdmin: Optional[bool] = False


players = {}


@router.post('/players/', tags=['Players'])
async def create_player(player: Player, db: Session = Depends(get_db)) -> Player:
    dbPlayerToAdd = DbPlayer(
        playerName=player.playerName,
        password=player.password,
        email=player.email,
        isAdmin=player.isAdmin,
    )
    db.add(dbPlayerToAdd)
    db.commit()
    db.refresh(dbPlayerToAdd)
    return dbPlayerToAdd


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
