from fastapi import APIRouter, HTTPException
import logging
from pydantic import BaseModel, Field
from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.models import get_db, DbTransaction

router = APIRouter()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)


class CreateTransaction(BaseModel):
    """Add a transaction"""
    amount: float = Field(
        ..., description=' Transaction amount, positive for deposits, negative for withdrawals.'
    )
    description: str


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


@router.post('/transactions', tags=['Transactions'], status_code=201, response_model=Transaction)
def create_transaction(transaction: CreateTransaction, db: Session = Depends(get_db)) -> Transaction:
    """Add Transaction to the database."""
    logging.debug(f'Create Transaction: {transaction}')
    dbTransactionToAdd = DbTransaction(amount=transaction.amount, description=transaction.description)
    try:
        db.add(dbTransactionToAdd)
        db.commit()
        db.refresh(dbTransactionToAdd)
        new_transaction = Transaction(id=dbTransactionToAdd.id, amount=dbTransactionToAdd.amount, description=dbTransactionToAdd.description)
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
