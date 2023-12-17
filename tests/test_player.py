from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from src.main import app
from database.models import get_db, DbPlayer
from alembic.config import Config
from alembic import command
client = TestClient(app)

TEST_DATABASE_URL = 'sqlite:///:memory:'
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Override the database session for testing."""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db

# Create the in-memory database
alembic_cfg = Config("alembic.ini")
alembic_cfg.set_main_option("script_location", "database/migrations")
command.upgrade(alembic_cfg, "head")

def test_create_player():
    # arrange
    data = {
            'playerName': 'test_player',
            'password': 'test_password',
            'email': 'test@nopace.com',
            'isAdmin': False,
        },

    # act
    response = client.post(
        '/players/',
        json = data,
    )

    # assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'
    assert response_data['email'] == 'test@nopace.com'
    assert response_data['isAdmin'] is False
    assert response_data['isActive'] is True

