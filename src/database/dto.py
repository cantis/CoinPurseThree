"""pydantic models for database objects"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


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
    isActive: bool = True


class Transaction(BaseModel):
    transactionId: int
    characterId: int
    amount: float = Field(..., precision=2)
    description: Optional[str] = None
    transactionDate: datetime