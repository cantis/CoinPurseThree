from fastapi import APIRouter
from fastapi.params import Depends
import logging
from pydantic import BaseModel, EmailStr

from sqlalchemy.orm.session import Session
from typing import Optional

from database.models import get_db, DbPlayer

router = APIRouter()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)


# region Pydantic Models
class CreatePlayer(BaseModel):
    """Create a player."""

    playerName: str
    password: str
    email: EmailStr
    isAdmin: Optional[bool] = False
    isActive: Optional[bool] = True


class UpdatePlayer(BaseModel):
    """Update a player."""

    playerName: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]
    isAdmin: Optional[bool]
    isActive: Optional[bool]


class Player(BaseModel):
    """Represents a player."""

    playerId: int
    playerName: str
    password: str
    email: EmailStr
    isAdmin: Optional[bool] = False
    isActive: Optional[bool] = True


# endregion


@router.post('/players/', tags=['Players'], status_code=201)
async def create_player(player: CreatePlayer, db: Session = Depends(get_db)) -> Player:
    logging.debug(f'Create Player: {player}')
    dbPlayerToAdd = DbPlayer(
        playerName=player.playerName,
        password=player.password,
        email=player.email,
        isAdmin=player.isAdmin,
    )
    logging.debug(f'Create Player: {player}')
    db.add(dbPlayerToAdd)
    db.commit()
    db.refresh(dbPlayerToAdd)
    return dbPlayerToAdd


@router.get('/players/{playerId}', tags=['Players'], status_code=200)
async def read_player(playerId: int, db: Session = Depends(get_db)):
    logging.debug(f'Read Player: {playerId}')
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == playerId).first()
    if db_player is None:
        return {'message': 'Player not found'}
    player = Player(
        playerId=db_player.playerId,
        playerName=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        isAdmin=db_player.isAdmin,
    )
    return player


@router.put('/players/{playerId}', tags=['Players'], status_code=200)
async def update_player(playerId: int, player: Player, db: Session = Depends(get_db)):
    logging.debug(f'Update Player: {playerId} {player}')
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == playerId).first()
    if db_player is None:
        return {'message': 'Player not found'}
    db_player.playerName = player.playerName
    db_player.password = player.password
    db_player.email = player.email
    db_player.isAdmin = player.isAdmin
    db.commit()
    db.refresh(db_player)
    player = Player(
        playerId=db_player.playerId,
        playerName=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        isAdmin=db_player.isAdmin,
    )
    return player


@router.delete('/players/{user_id}', tags=['Players'], status_code=204)
async def delete_player(user_id: int, db: Session = Depends(get_db)):
    logging.debug(f'Delete Player: {user_id}')
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
    logging.debug('Get All Players Endpoint')
    db_players = db.query(DbPlayer).all()
    players = []
    for db_player in db_players:
        player = Player(
            playerId=db_player.playerId,
            playerName=db_player.playerName,
            password=db_player.password,
            email=db_player.email,
            isAdmin=db_player.isAdmin,
        )
        players.append(player)
    return players
