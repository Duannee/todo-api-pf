import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from src.apps.core.database import get_session
from src.apps.core.security import get_password_hash
from src.apps.users.models import User, register_metadata
from src.main import app


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    register_metadata.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    register_metadata.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    password = "testtest"
    user = User(
        username="Test",
        email="teste@test.com",
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        "/token",
        data={"username": user.email, "password": user.clean_password},
    )
    return response.json()["access_token"]
