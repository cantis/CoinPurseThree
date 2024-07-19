"""SQLModel models for the database."""
from __future__ import annotations

import logging
import os
from contextlib import contextmanager
from datetime import datetime
from sqlite3 import DatabaseError
from typing import Generator

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables() -> None:
    """Create the database and tables."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Return a database session."""
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except DatabaseError as e:
            message = f'Database error {e.message}'
            logging.exception(message)
            session.rollback()
            raise


# table models
class Player(SQLModel, table=True):
    """Model for adding a player to the database."""

    player_id: int | None = Field(default=None, primary_key=True)
    player_name: str
    password: str
    email: str
    characters: list[Character] = Relationship(back_populates='player')
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)

class Character(SQLModel, table=True):
    """DB Model for a character in the game."""

    character_id: int | None = Field(default=None, primary_key=True)
    character_name: str
    player_id: int = Field(foreign_key='player.player_id')
    transactions: list[Transaction] = Relationship(back_populates='character')
    is_active: bool = Field(default=True)


class Transaction(SQLModel, table=True):
    """DB Model for a transaction."""

    transaction_id: int = Field(primary_key=True)
    transaction_date: datetime = Field(default=datetime.now)
    transaction_type: str = Field(default='purchase')
    character_id: int = Field(foreign_key='character.character_id')
    amount: int = Field()
    description: str = Field(default='')


# test models
class TestItem(SQLModel):
    """Model for the /test-validation endpoint."""

    name: str
    description: str = None
    price: float
    tax: float = None
