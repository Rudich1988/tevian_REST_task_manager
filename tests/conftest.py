import pytest
from dotenv import find_dotenv, load_dotenv


def pytest_configure(config):
    env_file = find_dotenv('.env.tests')
    load_dotenv(env_file)


@pytest.fixture(scope='function')
def db_session():
    from task_manager.db.db import Session
    with Session() as session:
        yield session
        session.rollback()


@pytest.fixture(scope='module')
def client():
    from task_manager.app import app
    app.testing = True
    with app.test_client() as client:
        yield client