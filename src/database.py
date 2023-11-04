from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydantic Models (DTOs)
class Player(BaseModel):
    userId: int
    playerName: str
    password: str
    email: EmailStr
    isAdmin: Optional[bool] = False


class Character(BaseModel):
    characterId: int
    characterName: str
    userId: int
    isActive: bool[bool] = True


class Transaction(BaseModel):
    transactionId: int
    characterId: int
    amount: float = Field(..., precision=2)
    description: Optional[str] = None
    transactionDate: datetime


class Base(DeclarativeBase):
    pass

# SQLAlchemy models
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
