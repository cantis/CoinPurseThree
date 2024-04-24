"""Players Router."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from database.models import DbPlayer, get_db
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel, EmailStr, Field

if TYPE_CHECKING:
    from sqlalchemy.orm.session import Session

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

    player_name: str = Field(
        ...,
        example='player1',
        description='The name of the player',
    )
    password: str = Field(..., example='password', description='password for player')
    email: EmailStr = Field(
        ...,
        example='someone@gmail.com',
        description='email for player',
    )
    is_admin: bool = Field(
        Optional=True,
        default=False,
        description='Is the player an admin (False)',
    )
    is_active: bool = Field(
        Optional=True,
        default=True,
        description='Is the player active (True)',
    )


class UpdatePlayer(BaseModel):
    """Update a player."""

    player_id: int = Field(..., example=1, description='The ID of the player')
    player_name: str = Field(
        ...,
        Optional=True,
        example='player1',
        description='The name of the player',
    )
    password: str = Field(
        ...,
        Optional=True,
        example='password',
        description='password for player',
    )
    email: EmailStr = Field(
        ...,
        Optional=True,
        example='someone@gmail.com',
        description='email for player',
    )
    is_admin: bool = Field(
        Optional=True,
        default=False,
        description='Is the player an admin (False)',
    )
    is_active: bool = Field(
        Optional=True,
        default=True,
        description='Is the player active (True)',
    )


class Player(BaseModel):
    """Represents a player."""

    player_id: int = Field(..., example=1, description='The ID of the player')
    player_name: str = Field(
        ...,
        example='player1',
        description='The name of the player',
    )
    password: str = Field(
        ...,
        example='password',
        description='The password for the player',
    )
    email: EmailStr = Field(
        ...,
        example='someone@gmail.com',
        description='The email for the player',
    )
    is_admin: bool = Field(
        Optional=True,
        default=False,
        description='Is the player an admin (False)',
    )
    is_active: bool = Field(
        Optional=True,
        default=True,
        description='Is the player active (True)',
    )


# endregion


@router.post('/players/', tags=['Players'], status_code=201, response_model=Player)
async def create_player(player: CreatePlayer, db: Session = Depends(get_db)) -> Player:
    """Create a player."""
    logging.debug('Create Player', extra={'player': player})
    db_player_to_add = DbPlayer(
        playerName=player.player_name,
        password=player.password,
        email=player.email,
        isAdmin=player.is_admin,
    )
    try:
        db.add(db_player_to_add)
        db.commit()
        db.refresh(db_player_to_add)
        new_player = Player(
            player_id=db_player_to_add.playerId,
            player_name=db_player_to_add.playerName,
            password=db_player_to_add.password,
            email=db_player_to_add.email,
            is_admin=db_player_to_add.isAdmin,
        )
        return new_player
    except Exception as e:
        logging.error(f'Error creating player: {e}')
        raise HTTPException(status_code=500, detail='Internal server error creating player.')


@router.get(
    '/players/{playerId}',
    tags=['Players'],
    status_code=200,
    response_model=Player,
    responses={404: {'description': 'Player \<id\> not found'}},
)
async def get_player(player_id: int, db: Session = Depends(get_db)) -> Player:
    """Get a player."""
    logging.debug('Read Player:', extra={'playerId': player_id})
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail=f'Player {player_id} not found')
    return Player(
        player_id=db_player.playerId,
        player_name=db_player.playerName,
        password=db_player.password,
        email=db_player.email,
        is_admin=db_player.isAdmin,
    )


@router.put(
    '/players/{playerId}',
    tags=['Players'],
    status_code=200,
    response_model=Player,
    responses={404: {'description': 'Player \<id\> not found to update'}},
)
async def update_player(player_id: int, updated_player: UpdatePlayer, db: Session = Depends(get_db)) -> Player:
    """Update a player."""
    logging.debug('Update Player', extra={'player_id': player_id, 'updated_player': updated_player})
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == player_id).first()
    if db_player is None:
        raise HTTPException(
            status_code=404,
            detail='Original player not found to update',
        )

    try:
        db_player.playerName = updated_player.player_name if updated_player.player_name else db_player.playerName
        db_player.password = updated_player.password if updated_player.password else db_player.password
        db_player.email = updated_player.email if updated_player.email else db_player.email
        db_player.isAdmin = updated_player.is_admin if updated_player.is_admin is not None else db_player.isAdmin
        db_player.isActive = updated_player.is_active if updated_player.is_active is not None else db_player.isActive
        db.commit()
        db.refresh(db_player)
        updated_player = Player(
            player_id=db_player.playerId,
            player_name=db_player.playerName,
            password=db_player.password,
            email=db_player.email,
            is_admin=db_player.isAdmin,
            is_active=db_player.isActive,
        )
    except Exception as e:
        logging.error(f'Error updating player: {e}')
        raise
    return updated_player


@router.delete('/players/{playerId}', tags=['Players'], status_code=204)
async def delete_player(player_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a player."""
    logging.debug('Delete Player:', extra={'playerId': player_id})
    db_player = db.query(DbPlayer).filter(DbPlayer.playerId == player_id).first()
    if db_player is None:
        raise HTTPException(status_code=404, detail='Player not found to delete')
    db.delete(db_player)
    db.commit()


@router.get('/players/', tags=['Players'], status_code=200, response_model=list[Player])
async def get_all_players(db: Session = Depends(get_db)) -> list[Player]:
    """Get all players."""
    logging.debug('Get All Players Endpoint')
    db_players = db.query(DbPlayer).all()
    players = []
    for db_player in db_players:
        player = Player(
            player_id=db_player.playerId,
            player_name=db_player.playerName,
            password=db_player.password,
            email=db_player.email,
            is_admin=db_player.isAdmin,
        )
        players.append(player)
    return players
