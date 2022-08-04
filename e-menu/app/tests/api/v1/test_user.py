import logging

from app.tests.conftest import EMAIL, PASSWORD


def test_create_user(client):
    logging.info("Test create user")
    data = {"email": EMAIL, "not_hashed_password": PASSWORD}
    response = client.post("/v1/create-user", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "test@user.com"
    # TODO add user with same email check 400
