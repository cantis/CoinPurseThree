from fastapi.testclient import TestClient
import os
from os import path
import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base, get_db
from src.main import app

TEST_DATABASE_URL = 'sqlite:///instance/coin_purse_temp_test.db'

client = TestClient(app) # fastapi test client

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
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='module', autouse=True)
def create_test_database():
    """Setup the database for the test session and teardown after"""

    # Note: as of 2024-03-07, migrations are not working with the in-memory database
    # so I'm working 'on disk' for now. This seems to be a known problem with alembic/sqlalchemy

    # Drop the database if it exists
    file_path = TEST_DATABASE_URL.removeprefix('sqlite:///')
    if path.exists(file_path):
        os.remove(file_path)

    # Create the database
    Base.metadata.create_all(engine)
    yield
    engine.dispose()
