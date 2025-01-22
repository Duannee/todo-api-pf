from sqlalchemy import create_engine
from sqlalchemy.orm import Session, registry

from src.apps.core.settings import Settings

register_metadata = registry()

engine = create_engine(Settings().DATABASE_URL)

register_metadata.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
