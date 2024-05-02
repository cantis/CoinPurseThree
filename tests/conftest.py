"""Configuration for the test suite."""
import logging

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.database.models import Base, DbCharacter, DbPlayer, get_db
from src.main import app

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='coinpurse.log',
    filemode='a',
    level=logging.DEBUG,
)

# TEST_DATABASE_URL = 'sqlite:///:memory:'
TEST_DATABASE_URL = 'sqlite:///coin_purse_test.db'

client = TestClient(app)  # fastapi test client

logging.debug('Test Database URL: %s', TEST_DATABASE_URL)
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    },
    poolclass=StaticPool,
)
logging.DEBUG('Engine created: %s', engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This method and the dependency_overide below, override the get_db method in the main.py file for testing
# this works like a mock, but it's not a mock. It's a real database session that is used for testing
def override_get_db():  # noqa: ANN201
    """Override the database session for testing."""
    with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def _create_test_database():
    """Create database for the test session and teardown after."""
    # Create the database
    Base.metadata.create_all(engine)
    yield
    engine.dispose()


@pytest.fixture()
def _add_test_player() -> None:
    """Add a player to the database for testing."""
    db: Session = TestingSessionLocal()
    player_to_add = DbPlayer(
        playerName='test_player',
        password='test_password',  # noqa: S106
        email='test@noplace.com',
        isAdmin=False,
        isActive=True,
    )
    db.add(player_to_add)
    db.commit()


@pytest.fixture()
def _add_test_characters(_add_test_player) -> None:
    """Add two characters to the database for testing."""
    db: Session = TestingSessionLocal()
    character_one_to_add = DbCharacter(characterName='Character 1', playerId=1, isActive=True)
    character_two_to_add = DbCharacter(characterName='Character 2', playerId=1, isActive=True)
    db.add(character_one_to_add)
    db.add(character_two_to_add)
    db.commit()
