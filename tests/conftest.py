import pytest
from sqlmodel import Session
from fastapi.testclient import TestClient
from task_manager.db import DB
from task_manager.model import Tasks, TaskStatus
from task_manager.main import app


@pytest.fixture
def task1():
    """
    Create a Task 1
    """
    task1 = Tasks(
        status=TaskStatus.NOT_STARTED,
    )
    yield task1


@pytest.fixture
def task2():
    """
    Create a Task 2
    """
    task2 = Tasks(
        status=TaskStatus.NOT_STARTED,
    )
    yield task2

@pytest.fixture
def task3():
    """
    Create a Task 3
    """
    task3 = Tasks(
        status=TaskStatus.NOT_STARTED,
        validation_error="Invalid IP range: 192.168.1.256"
    )
    yield task3


@pytest.fixture
def db_instance(scope="session"):
    """
    Create a DB Instance
    """
    db = DB()
    yield db


@pytest.fixture
def session(db_instance, scope="session"):
    """
    Create a Session, close after test session, uses `db_instance` fixture
    """
    session = Session(db_instance.engine)
    yield session
    session.close()

@pytest.fixture(scope="function")
def test_client(session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    # def override_get_db():
    #     try:
    #         yield session
    #     finally:
    #         session.close()

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_instance_empty(db_instance, session, scope="function"):
    """
    Create an Empty DB Instance, uses `db_instance` and `session` fixtures
    """
    # Clear DB before test function
    db_instance.delete_all_tasks(session=session)
    yield db_instance

    # Clear DB after test function
    db_instance.delete_all_tasks(session=session)