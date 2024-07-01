"""SQLModel models for the database."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Generator

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

if TYPE_CHECKING:
    from decimal import Decimal, Enum
import os

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


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


class CharacterBase(SQLModel):
    """DB Model for a character in the game."""

    character_name: str
    player_id: int = Field(foreign_key='player.player_id')
    is_active: bool = Field(default=True)


class Character(CharacterBase, table=True):
    """Character table model for the database."""

    character_id: int = Field(primary_key=True)


class TransactionBase(SQLModel):
    """DB Model for a transaction."""

    character_id: int = Field(foreign_key='character.character_id')
    amount: int = Field()
    description: str = Field(default='')


class Transaction(TransactionBase, table=True):
    """Transaction table model for the database."""

    transaction_id: int = Field(primary_key=True)
    transaction_date: datetime = Field(default=datetime.now)


class TestItem(SQLModel):
    """Model for the /test-validation endpoint."""

    name: str
    description: str = None
    price: float
    tax: float = None
