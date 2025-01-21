from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.apps.core.settings import Settings
from sqlalchemy.orm import registry

register_metadata = registry()

engine = create_engine(Settings().DATABASE_URL)

register_metadata.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
