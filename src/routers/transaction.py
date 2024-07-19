"""Transaction router."""
from __future__ import annotations

import datetime
import logging
from typing import TYPE_CHECKING

from fastapi import APIRouter, Depends, HTTPException
from models import Transaction
from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

router = APIRouter()


# class CreateTransaction(BaseModel):
#     """Add a transaction."""

#     character_id: int = Field(
#         ...,
#         Optional=True,
#         description='The ID of the character that the transaction is for.',
#     )
#     amount: float = Field(
#         ...,
#         description=' Transaction amount, positive for deposits, negative for withdrawals.',
#         precision=2,
#     )
#     description: str = Field(
#         ..., Optional=True, description='Description of the transaction.'
#     )


# class Transaction(BaseModel):
#     """Represents a transaction, adding or removing funds from a character's wallet."""

#     id: int
#     amount: float = Field(
#         ..., description='Positive for deposits, negative for withdrawals.'
#     )
#     description: str


# transactions = []


# @router.get('/transactions', tags=['Transactions'])
# def get_transactions() -> list[Transaction]:
#     """Get all transactions."""
#     return transactions


# @router.get('/transactions/{transaction_id}', tags=['Transactions'])
# def get_transaction(transaction_id: int) -> dict[str, str] | Transaction:
#     """Get a transaction by ID."""
#     for transaction in transactions:
#         if transaction.id == transaction_id:
#             return transaction
#     return {'message': 'Transaction not found'}


# @router.post(
#     '/transactions/', tags=['Transactions'], status_code=201, response_model=Transaction,
# )
# async def create_transaction(
#     transaction: CreateTransaction, db: Session = Depends(get_db)
# ) -> Transaction:
#     """Add Transaction to the database."""
#     logging.debug('Create Transaction:', extra={'transaction': transaction})
#     db_transaction_to_add = DbTransaction(
#         character_id=transaction.character_id,
#         amount=transaction.amount,
#         description=transaction.description,
#         transaction_date=datetime.now(),
#     )
#     try:
#         db.add(db_transaction_to_add)
#         db.commit()
#         db.refresh(db_transaction_to_add)
#         return Transaction(
#             transaction_id=db_transaction_to_add.transaction_id,
#             character_id=db_transaction_to_add.character_id,
#             amount=db_transaction_to_add.amount,
#             description=db_transaction_to_add.description,
#             transaction_date=db_transaction_to_add.transaction_date,
#         )
#     except Exception as e:
#         logging.error(f'Error creating transaction: {e}')
#         raise HTTPException(status_code=500, detail='Error creating transaction')


# @router.put('/transactions/{transaction_id}', tags=['Transactions'])
# def update_transaction(transaction_id: int, updated_transaction: Transaction) -> dict[str, str]:
#     """Update a transaction."""
#     for i, transaction in enumerate(transactions):
#         if transaction.id == transaction_id:
#             transactions[i] = updated_transaction
#             return {'message': 'Transaction updated successfully'}
#     return {'message': 'Transaction not found'}


# @router.delete('/transactions/{transaction_id}', tags=['Transactions'])
# def delete_transaction(transaction_id: int) -> dict[str, str]:
#     """Delete a transaction."""
#     for i, transaction in enumerate(transactions):
#         if transaction.id == transaction_id:
#             del transactions[i]
#             return {'message': 'Transaction deleted successfully'}
#     return {'message': 'Transaction not found'}
