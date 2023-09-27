from fastapi import FastAPI

from src.routers.characters import router as characters_router
from src.routers.players import router as players_router
from src.routers.transaction import router as transaction_router

app = FastAPI(
    title='Coinpurse API',
    description='An API to manage an RPG character\'s coinpurse. Records purchases and sales of items and current balance of coins.',
    version='0.0.1',
)

app.include_router(
    characters_router,
    tags=['Characters'],
)

app.include_router(
    players_router,
    tags=['Players'],
)

app.include_router(
    transaction_router,
    tags=['Transactions'],
)
