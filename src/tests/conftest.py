from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.api.deps import get_db
from src.core.config import settings
from src.database.init_db import init_db
from src.database.session import Base
from src.main import app

engine = create_engine(settings.TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

init_db(db=TestingSessionLocal())


@pytest.fixture(scope="session")
def db() -> Generator:
    yield TestingSessionLocal()
