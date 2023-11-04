from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from src.routers.characters import router as characters_router
# from src.routers.players import router as players_router
# from src.routers.transaction import router as transaction_router

from database import Base

DATABASE_URL = "sqlite:///./coin_purse.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


# Dependency to get the database session
def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)


# app.include_router(
#     players_router,
#     prefix="/players",
#     tags=["players"],
#     responses={404: {"description": "Not found"}},
# )

# app.include_router(
#     characters_router,
#     prefix="/characters",
#     tags=["characters"],
#     responses={404: {"description": "Not found"}},
# )

# app.include_router(
#     transaction_router,
#     prefix="/transactions",
#     tags=["transactions"],
#     responses={404: {"description": "Not found"}},
# )

# App Running check
@app.get("/")
async def root():
    return {"message": "Hello World"}