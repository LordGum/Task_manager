import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_todo(db_session):
    from app import models

    todo = models.Todo(
        title="Test Task",
        description="Test Description",
        status="в ожидании",
        priority=5
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)
    return todo