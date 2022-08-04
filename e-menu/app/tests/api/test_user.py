import logging

from app.tests.conftest import EMAIL, PASSWORD

DATA = {"email": EMAIL, "not_hashed_password": PASSWORD}


def test_create_user(client):
    logging.info("Test create user")
    data = DATA
    response = client.post("/v1/create-user", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@user.com"


def test_user_already_exists(client):
    data = DATA
    response = client.post("/v1/create-user", json=data)
    assert response.status_code == 400
    assert response.json()["detail"] == "The user with this email already exists in database."


def test_unauthorized_user(
    client,
):
    response = client.post("/v1/access-token", data={"username": EMAIL, "password": PASSWORD})
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens

    response = client.post("/v1/access-token", data={"username": EMAIL, "password": "bad_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"
