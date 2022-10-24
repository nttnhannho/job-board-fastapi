import os
import sys
from typing import Any
from typing import Generator

import pytest
from apis.base import api_router
from core.config import settings
from db.base import Base
from db.session import get_db
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from tests.utils.users import authentication_token_from_email


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_job_board_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def start_application():
    app = FastAPI()
    app.include_router(api_router)

    return app


@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    app_ = start_application()
    yield app_
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def db_session(app: FastAPI) -> Generator[SessionTesting, Any, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(
    app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db_session: Session):
    return authentication_token_from_email(
        client=client,
        email=settings.TEST_USER_EMAIL,
        db=db_session,
    )
