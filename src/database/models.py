"""Sqlalchemy models for the database."""
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

DATABASE_URL = 'sqlite:///../instance/coin_purse.db'
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    """Get a database session."""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


class DbPlayer(Base):
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
