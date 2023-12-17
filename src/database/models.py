"""Sqlalchemy models for the database."""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DbPlayer(Base):
    """DB Model for a player in the game."""
    __tablename__ = 'players'

    userId = Column(Integer, primary_key=True)
    playerName = Column(String)
    password = Column(String)
    email = Column(String)
    isAdmin = Column(Boolean, default=False)
    isActive = Column(Boolean, default=True)


class DbCharacter(Base):
    """DB Model for a character in the game."""
    __tablename__ = 'characters'

    characterId = Column(Integer, primary_key=True)
    characterName = Column(String)
    playerId = Column(Integer)
    isActive = Column(Boolean, default=True)


class DbTransaction(Base):
    """DB Model for a transaction in the game."""
    __tablename__ = 'transactions'

    transactionId = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    amount = Column(Float(precision=2))
    description = Column(String)
    transactionDate = Column(DateTime)
