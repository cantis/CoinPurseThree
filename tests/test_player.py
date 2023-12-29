from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from os import environ, path
import pytest
from sqlalchemy import create_engine, StaticPool, inspect
from sqlalchemy.orm import sessionmaker

from src.main import app, logger
from database.models import get_db
from alembic import op
import sqlalchemy as sa

# logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     filename='../migration.log',
#                     filemode='a',
#                     )
# logging.info('Starting tests')
# logger = logging.getLogger('alembic')
# logging.getLogger('alembic').setLevel(logging.DEBUG)

logger.debug('Starting tests')

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

# This method and the dependency_overide, overrides the get_db method in the main.py file
def override_get_db():
    """Override the database session for testing."""
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db


# Setup the database for testing
@pytest.fixture(scope='session', autouse=True)
def apply_migrations():
    """Setup the database for testing."""
    logger.debug('Applying migrations')
    engine = create_engine(TEST_DATABASE_URL)
    with engine.begin() as connection:
        alembic_cfg = Config('alembic.ini')
        alembic_cfg.attributes['configure_logger'] = True
        alembic_cfg.attributes['connection'] = connection
        alembic_cfg.set_main_option('script_location', './src/alembic')
        try:
            command.ensure_version(alembic_cfg)
            command.upgrade(alembic_cfg, 'heads')
            connection.commit()
        except Exception as e:
            print(f'Exception: {e}')

        assert inspect(engine).has_table('players') is True
        yield
        engine.dispose()

def test_create_player():
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
