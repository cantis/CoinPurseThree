from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
import logging
import os
from os import path
import pytest
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from src.main import app
from database.models import get_db, Base


LOG_PATH = path.join(path.dirname(path.abspath(__file__)), '../tests/test.log')
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=LOG_PATH,
    filemode='a',
    level=logging.DEBUG,
)
logging.debug('Test Initalize')

client = TestClient(app)

# TEST_DATABASE_URL = 'sqlite:///:memory:'
TEST_DATABASE_URL = 'sqlite:///instance/coin_purse_temp_test.db'

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={
        'check_same_thread': False,
    },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# This method and the dependency_overide below, override the get_db method in the main.py file for testing
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
    """Setup the database for testing."""

    # # Drop the database
    logging.debug('Dropping the database')
    file_path = TEST_DATABASE_URL.removeprefix('sqlite:///')
    if path.exists(file_path):
        os.remove(file_path)

    # Create the database
    logging.debug('Applying migrations')
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    yield
    engine.dispose()
    # alembic_cfg = Config()
    # with engine.begin() as connection:
        # alembic_cfg.attributes['connection'] = connection
        # alembic_cfg.set_main_option('sqlalchemy.url', TEST_DATABASE_URL)
        # alembic_cfg.set_main_option('script_location', './src/alembic')
        # try:

        #     # command.upgrade(alembic_cfg, 'head')
        # except Exception as e:
        #     logging.error(f'Exception during migration: {e}')
        #     raise e
        # yield
        # Clean up
        # engine.dispose()
        # logging.debug('Dropping the database')
        # if path.exists(file_path):
        #     os.remove(file_path)


def test_create_player(create_test_database: None) -> None:
    # arrange
    data = {
        'playerName': 'test_player',
        'password': 'test_password',
        'email': 'test@noplace.com',
        'isAdmin': False,
    }

    # act
    # inspector = inspect(engine)
    # tables = inspector.get_table_names()

    response = client.post(
        '/players/',
        json=data,
    )

    # assert
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'
    assert response_data['email'] == 'test@noplace.com'
    assert response_data['isAdmin'] is False


def test_get_player(create_test_database: None) -> None:
    # arrange

    # act
    response = client.get('/players/1')

    # assert
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['playerId'] == 1
    assert response_data['playerName'] == 'test_player'
    assert response_data['password'] == 'test_password'
    assert response_data['email'] == 'test@noplace.com'
    assert response_data['isAdmin'] is False
