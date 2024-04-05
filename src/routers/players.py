from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
import logging
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm.session import Session

from src.database.models import get_db, DbPlayer


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

    playerName: str = Field(
        ..., example='player1', description='The name of the player'
    )
    password: str = Field(..., example='password', description='password for player')
    email: EmailStr = Field(
        ..., example='someone@gmail.com', description='email for player'
    )
    isAdmin: bool = Field(
        Optional=True, default=False, description='Is the player an admin (False)'
    )
    isActive: bool = Field(
        Optional=True, default=True, description='Is the player active (True)'
    )


class UpdatePlayer(BaseModel):
    """Update a player."""

    playerId: int = Field(..., example=1, description='The ID of the player')
    playerName: str = Field(
        ..., Optional=True, example='player1', description='The name of the player'
    )
    password: str = Field(
        ..., Optional=True, example='password', description='password for player'
    )
    email: EmailStr = Field(
        ..., Optional=True, example='someone@gmail.com', description='email for player'
    )
    isAdmin: bool = Field(
        Optional=True, default=False, description='Is the player an admin (False)'
    )
    isActive: bool = Field(
        Optional=True, default=True, description='Is the player active (True)'
    )


class Player(BaseModel):
    """Represents a player."""

    playerId: int = Field(..., example=1, description='The ID of the player')
    playerName: str = Field(
        ..., example='player1', description='The name of the player'
    )
    password: str = Field(
        ..., example='password', description='The password for the player'
    )
    email: EmailStr = Field(
        ..., example='someone@gmail.com', description='The email for the player'
    )
    isAdmin: bool = Field(
        Optional=True, default=False, description='Is the player an admin (False)'
    )
    isActive: bool = Field(
        Optional=True, default=True, description='Is the player active (True)'
    )


# endregion


@router.post('/players/', tags=['Players'], status_code=201, response_model=Player)
async def create_player(player: CreatePlayer, db: Session = Depends(get_db)) -> Player:
    """Create a player."""
    logging.debug(f'Create Player: {player}')
    dbPlayerToAdd = DbPlayer(
        playerName=player.playerName,
        password=player.password,
        email=player.email,
        isAdmin=player.isAdmin,
    )
    try:
        db.add(dbPlayerToAdd)
        db.commit()
        db.refresh(dbPlayerToAdd)
        new_player = Player(
            playerId=dbPlayerToAdd.playerId,
            playerName=dbPlayerToAdd.playerName,
            password=dbPlayerToAdd.password,
            email=dbPlayerToAdd.email,
            isAdmin=dbPlayerToAdd.isAdmin,
        )
        return new_player
    except Exception as e:
        logging.error(f'Error creating player: {e}')
        raise HTTPException(
            status_code=500, detail='Internal server error creating player.'
        )


@router.get(
    '/players/{playerId}',
    tags=['Players'],
    status_code=200,
    response_model=Player,
    responses={404: {'description': 'Player \<id\> not found'}},
)
async def get_player(playerId: int, db: Session = Depends(get_db)) -> Player:
    """Get a player."""
    logging.debug(f'Read Player: {playerId}')
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == playerId).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail=f'Player {playerId} not found')
    player = Player(
        playerId=db_player.playerId,
        playerName=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        isAdmin=db_player.isAdmin,
    )
    return player


@router.put(
    '/players/{playerId}',
    tags=['Players'],
    status_code=200,
    response_model=Player,
    responses={404: {'description': 'Player \<id\> not found to update'}},
)
async def update_player(
    playerId: int, updated_player: UpdatePlayer, db: Session = Depends(get_db)
) -> Player:
    """Update a player."""
    logging.debug(f'Update Player: {playerId} {updated_player}')
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == playerId).first()
    if db_player is None:
        raise HTTPException(
            status_code=404, detail='Original player not found to update'
        )

    try:
        db_player.playerName = (
            updated_player.playerName
            if updated_player.playerName
            else db_player.playerName
        )
        db_player.password = (
            updated_player.password if updated_player.password else db_player.password
        )
        db_player.email = (
            updated_player.email if updated_player.email else db_player.email
        )
        db_player.isAdmin = (
            updated_player.isAdmin
            if updated_player.isAdmin is not None
            else db_player.isAdmin
        )
        db_player.isActive = (
            updated_player.isActive
            if updated_player.isActive is not None
            else db_player.isActive
        )
        db.commit()
        db.refresh(db_player)
        updated_player = Player(
            playerId=db_player.playerId,
            playerName=db_player.playerName,
            password=db_player.password,
            email=db_player.email,
            isAdmin=db_player.isAdmin,
            isActive=db_player.isActive,
        )
    except Exception as e:
        logging.error(f'Error updating player: {e}')
        raise
    return updated_player


@router.delete('/players/{playerId}', tags=['Players'], status_code=204)
async def delete_player(playerId: int, db: Session = Depends(get_db)):
    """Delete a player."""
    logging.debug(f'Delete Player: {playerId}')
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == playerId).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail='Player not found to delete')
    db.delete(db_player)
    db.commit()
    return


@router.get('/players/', tags=['Players'], status_code=200, response_model=list[Player])
async def get_all_players(db: Session = Depends(get_db)):
    """Get all players."""
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
