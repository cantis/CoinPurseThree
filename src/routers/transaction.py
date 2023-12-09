from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class Transaction(BaseModel):
    id: int
    amount: float
    description: str

transactions = []

@router.get("/transactions", tags=["Transactions"])
def get_transactions():
    return transactions

@router.get("/transactions/{transaction_id}", tags=["Transactions"])
def get_transaction(transaction_id: int):
    for transaction in transactions:
        if transaction.id == transaction_id:
            return transaction
    return {"message": "Transaction not found"}

@router.post("/transactions", tags=["Transactions"])
def create_transaction(transaction: Transaction):
    transactions.append(transaction)
    return {"message": "Transaction created successfully"}

@router.put("/transactions/{transaction_id}", tags=["Transactions"])
def update_transaction(transaction_id: int, updated_transaction: Transaction):
    for i, transaction in enumerate(transactions):
        if transaction.id == transaction_id:
            transactions[i] = updated_transaction
            return {"message": "Transaction updated successfully"}
    return {"message": "Transaction not found"}

@router.delete("/transactions/{transaction_id}", tags=["Transactions"])
def delete_transaction(transaction_id: int):
    for i, transaction in enumerate(transactions):
        if transaction.id == transaction_id:
            del transactions[i]
            return {"message": "Transaction deleted successfully"}
    return {"message": "Transaction not found"}
