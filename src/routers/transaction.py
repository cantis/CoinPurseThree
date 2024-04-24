import datetime
from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel, Field
from fastapi import Depends
from sqlalchemy.orm import Session

from database.models import get_db, DbTransaction

router = APIRouter()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)


class CreateTransaction(BaseModel):
    """Add a transaction"""
    character_id: int = Field(
        ...,
        Optional=True,
        description='The ID of the character that the transaction is for.',
    )
    amount: float = Field(
        ...,
        description=' Transaction amount, positive for deposits, negative for withdrawals.',
        precision=2,
    )
    description: str = Field(
        ..., Optional=True, description='Description of the transaction.'
    )


class Transaction(BaseModel):
    """Represents a transaction, adding or removing funds from a character's wallet."""
    id: int
    amount: float = Field(
        ..., description='Positive for deposits, negative for withdrawals.'
    )
    description: str


transactions = []


@router.get('/transactions', tags=['Transactions'])
def get_transactions():
    return transactions


@router.get('/transactions/{transaction_id}', tags=['Transactions'])
def get_transaction(transaction_id: int):
    for transaction in transactions:
        if transaction.id == transaction_id:
            return transaction
    return {'message': 'Transaction not found'}


@router.post(
    '/transactions/', tags=['Transactions'], status_code=201, response_model=Transaction
)
async def create_transaction(
    transaction: CreateTransaction, db: Session = Depends(get_db)
) -> Transaction:
    """Add Transaction to the database."""
    logging.debug(f'Create Transaction: {transaction}')
    dbTransactionToAdd = DbTransaction(
        character_id=transaction.character_id,
        amount=transaction.amount,
        description=transaction.description,
        transaction_date=datetime.now(),
    )
    try:
        db.add(dbTransactionToAdd)
        db.commit()
        db.refresh(dbTransactionToAdd)
        new_transaction = Transaction(
            transaction_id=dbTransactionToAdd.transaction_id,
            character_id=dbTransactionToAdd.character_id,
            amount=dbTransactionToAdd.amount,
            description=dbTransactionToAdd.description,
            transaction_date=dbTransactionToAdd.transaction_date,
        )
        return new_transaction
    except Exception as e:
        logging.error(f'Error creating transaction: {e}')
        raise HTTPException(status_code=500, detail='Error creating transaction')


@router.put('/transactions/{transaction_id}', tags=['Transactions'])
def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for i, transaction in enumerate(transactions):
        if transaction.id == transaction_id:
            transactions[i] = updated_transaction
            return {'message': 'Transaction updated successfully'}
    return {'message': 'Transaction not found'}


@router.delete('/transactions/{transaction_id}', tags=['Transactions'])
def delete_transaction(transaction_id: int):
    for i, transaction in enumerate(transactions):
        if transaction.id == transaction_id:
            del transactions[i]
            return {'message': 'Transaction deleted successfully'}
    return {'message': 'Transaction not found'}
