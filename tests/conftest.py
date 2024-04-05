from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.database.models import Base, DbPlayer, DbCharacter, get_db
from src.main import app

TEST_DATABASE_URL = 'sqlite:///:memory:'

client = TestClient(app)  # fastapi test client

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This method and the dependency_overide below, override the get_db method in the main.py file for testing
# this works like a mock, but it's not a mock. It's a real database session that is used for testing
def override_get_db():
    """Override the database session for testing."""
    with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope='function', autouse=True)
def create_test_database():
    """Setup the database for the test session and teardown after"""

    # Create the database
    Base.metadata.create_all(engine)
    yield
    engine.dispose()

@pytest.fixture(scope='function')
def add_test_player():
    """Add a player to the database for testing."""
    db: Session = TestingSessionLocal()
    player_to_add = DbPlayer(
        playerName='test_player',
        password='test_password',
        email='test@noplace.com',
        isAdmin=False,
        isActive=True,
    )
    db.add(player_to_add)
    db.commit()

@pytest.fixture(scope='function')
def add_test_characters(add_test_player):
    """Add two characters to the database for testing."""
    db: Session = TestingSessionLocal()
    character_one_to_add = DbCharacter(
        characterName='Character 1',
        playerId=1,
        isActive=True
    )
    character_two_to_add = DbCharacter(
        characterName='Character 2',
        playerId=1,
        isActive=True
    )
    db.add(character_one_to_add)
    db.add(character_two_to_add)
    db.commit()



