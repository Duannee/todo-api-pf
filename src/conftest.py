import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.apps.users.models import register_metadata


from src.main import app


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    register_metadata.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    register_metadata.metadata.drop_all(engine)
