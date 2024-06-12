"""SQLModel models for the database."""
from __future__ import annotations
from datetime import datetime
from typing import Generator

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

DATABASE_URL = 'sqlite:///../instance/coin_purse.db'
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, any, None]:
    """Get a new session for the database."""
    with Session(engine) as session:
        yield session

class PlayerBase(SQLModel):
    """Model for adding a player to the database."""

    player_name: str
    password: str
    email: str
    is_admin: bool = False
    is_active: bool = True


class Player(PlayerBase, table=True):
    """Player table model for the database."""

    player_id: int = Field(primary_key=True)
    characters: list[Character] = Relationship(back_populates='player')


class CharacterBase(SQLModel):
    """DB Model for a character in the game."""

    character_name: str
    player_id: int = Field(foreign_key='player.player_id')
    is_active = bool = True


class Character(CharacterBase, table=True):
    """Character table model for the database."""

    character_id: int = Field(primary_key=True)
    player: Player = Relationship(back_populates='characters')


class TransactionBase(SQLModel):
    """DB Model for a transaction in the game."""

    character_id: int = Field(foreign_key='character.character_id')
    amount: float = Field(precision=2)
    description: str


class Transaction(TransactionBase, table=True):
    """Transaction table model for the database."""

    transaction_id: int = Field(primary_key=True)
    transaction_date: datetime = Field(default=datetime.now)
    character: Character = Relationship(back_populates='transactions')
