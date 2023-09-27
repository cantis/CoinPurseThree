from decimal import Decimal

import fastapi
from fastapi import Path
from pydantic import BaseModel

router = fastapi.APIRouter()

class Transaction(BaseModel):
    character_id: int
    item: int
    price: Decimal
    is_sale: bool = False

transactions = []


@router.get('/buy/')
async def buy():
    '''Remove money from player, optional: record item in inventory'''
    return {'message': 'buy'}


@router.get('/sell/')
async def sell():
    '''Add money to player, optional: remove item from inventory'''
    return {'message': 'sell'}