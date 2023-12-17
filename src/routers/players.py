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


@router.post('/players/', tags=['Players'], status_code=201)
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


@router.get('/players/{user_id}', tags=['Players'], status_code=200)
async def read_player(user_id: int, db: Session = Depends(get_db)):
    db_player = db.query(DbPlayer).filter(DbPlayer.userId == user_id).first()
    if db_player is None:
        return {'message': 'Player not found'}
    player = Player(
        userId=db_player.userId,
        playerName=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        isAdmin=db_player.isAdmin,
    )
    return player


@router.put('/players/{user_id}', tags=['Players'], status_code=200)
async def update_player(user_id: int, player: Player, db: Session = Depends(get_db)):
    db_player = db.query(DbPlayer).filter(DbPlayer.userId == user_id).first()
    if db_player is None:
        return {'message': 'Player not found'}
    db_player.playerName = player.playerName
    db_player.password = player.password
    db_player.email = player.email
    db_player.isAdmin = player.isAdmin
    db.commit()
    db.refresh(db_player)
    player = Player(
        userId=db_player.userId,
        playerName=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        isAdmin=db_player.isAdmin,
    )
    return player


@router.delete('/players/{user_id}', tags=['Players'], status_code=204)
async def delete_player(user_id: int, db: Session = Depends(get_db)):
    db_player = db.query(DbPlayer).filter(DbPlayer.userId == user_id).first()
    if db_player is None:
        return {'message': 'Player not found'}
    db.delete(db_player)
    db.commit()
    player = Player(
        userId=db_player.userId,
        playerName=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        isAdmin=db_player.isAdmin,
    )
    return player


@router.get('/players/', tags=['Players'], status_code=200)
async def get_all_players(db: Session = Depends(get_db)):
    db_players = db.query(DbPlayer).all()
    players = []
    for db_player in db_players:
        player = Player(
            userId=db_player.userId,
            playerName=db_player.playerName,
            password=db_player.password,
            email=db_player.email,
            isAdmin=db_player.isAdmin,
        )
        players.append(player)
    return players
