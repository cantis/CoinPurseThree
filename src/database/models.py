"""Sqlalchemy models for the database."""
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DbPlayer(Base):
    __tablename__ = 'players'

    userId = Column(Integer, primary_key=True)
    playerName = Column(String)
    password = Column(String)
    email = Column(String)
    isAdmin = Column(Boolean, default=False)


class DbCharacter(Base):
    __tablename__ = 'characters'

    characterId = Column(Integer, primary_key=True)
    characterName = Column(String)
    userId = Column(Integer)
    isActive = Column(Boolean, default=True)


class DbTransaction(Base):
    __tablename__ = 'transactions'

    transactionId = Column(Integer, primary_key=True)
    characterId = Column(Integer)
    amount = Column(Float(precision=2))
    description = Column(String)
    transactionDate = Column(DateTime)