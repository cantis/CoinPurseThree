from fastapi.params import Depends
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker, Session

from database.models import Base, DbPlayer, get_db
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
    test_db: Session = TestingSessionLocal()
    new_player = DbPlayer(
        playerName='test_player',
        password='monday1',
        email='someone@gmail.com',
        isAdmin=False,
        isActive=True,
    )
    try:
        test_db.add(new_player)
        test_db.commit()
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {str(e)}")
