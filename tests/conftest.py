"""Configuration for the test suite."""
# import logging
# from typing import Generator

# import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

# from src.routers import characters, players, transaction
# from sqlmodel import Session, StaticPool, create_engine, sessionmaker


def create_test_app() -> 'FastAPI':
    """Create a FastAPI app for testing."""
    app = FastAPI(
        openapi_url='/api/v1/openapi.json',
    )
    # app.include_router(players.router)
    # app.include_router(characters.router)
    # app.include_router(transaction.router)
    return app


test_app = create_test_app()
test_client = TestClient(test_app)


# logging.basicConfig(
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filename='coinpurse.log',
#     filemode='a',
#     level=logging.DEBUG,
# )

# TEST_DATABASE_URL = 'sqlite:///:memory:'
# TEST_DATABASE_URL = 'sqlite:///coin_purse_test.db'

# logging.debug('Test Database URL: %s', TEST_DATABASE_URL)
# engine = create_engine(
#     TEST_DATABASE_URL,
#     connect_args={
#         'check_same_thread': False,
#     },
#     poolclass=StaticPool,
# )
# logging.debug('Engine created: %s', engine)

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# # This method and the dependency_overide below, override the get_db method in the main.py file for testing
# # this works like a mock, but it's not a mock. It's a real database session that is used for testing
# def override_get_db():  # noqa: ANN201
#     """Override the database session for testing."""
#     with TestingSessionLocal() as session:
#         yield session


# app.dependency_overrides[get_db] = override_get_db


# @pytest.fixture(autouse=True)
# def _create_test_database() -> Generator[None, any, None]:
#     """Create database for the test session and teardown after."""
#     # Create the database
#     Base.metadata.create_all(engine)
#     yield
#     engine.dispose()


# @pytest.fixture()
# def _add_test_player() -> None:
#     """Add a player to the database for testing."""
#     db: Session = TestingSessionLocal()
#     player_to_add = DbPlayer(
#         playerName='test_player',
#         password='test_password',  # noqa: S106
#         email='test@noplace.com',
#         isAdmin=False,
#         isActive=True,
#     )
#     db.add(player_to_add)
#     db.commit()


# @pytest.fixture()
# def _add_test_characters(_add_test_player) -> None:
#     """Add two characters to the database for testing."""
#     db: Session = TestingSessionLocal()
#     character_one_to_add = DbCharacter(characterName='Character 1', playerId=1, isActive=True)
#     character_two_to_add = DbCharacter(characterName='Character 2', playerId=1, isActive=True)
#     db.add(character_one_to_add)
#     db.add(character_two_to_add)
#     db.commit()
