from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.default import router as default_router
from app.api.dependencies import get_db
from app.api.v1.routers import router as api_router
from app.crud.user import UserCreate, create, get_user
from app.database.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

PASSWORD = "testpassword"
EMAIL = "test@user.com"


@pytest.fixture(scope="module")
def app() -> Generator:
    Base.metadata.create_all(bind=engine)
    app = FastAPI()
    app.include_router(api_router, prefix="/v1")
    app.include_router(default_router)
    yield app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def db_test_session(app: FastAPI) -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def client(db_test_session: TestingSessionLocal, app: FastAPI) -> Generator:
    def get_test_db() -> Generator:
        try:
            yield db_test_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as c:
        yield c


def user_authentication_header(client: TestClient, email: str, password: str):
    data = {"username": email, "password": password}
    r = client.post("v1/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    header = {"Authorization": f"Bearer {auth_token}"}
    return header


@pytest.fixture(scope="module")
def user_token_header(client: TestClient, db_test_session: TestingSessionLocal):
    user = get_user(email=EMAIL, db=db_test_session)
    if not user:
        test_user = UserCreate(email=EMAIL, not_hashed_password=PASSWORD)
        user = create(user_in=test_user, db=db_test_session)
    return user_authentication_header(client=client, email=EMAIL, password=PASSWORD)
