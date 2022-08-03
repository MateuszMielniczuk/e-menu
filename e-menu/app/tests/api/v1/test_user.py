import json


def test_create_user(client):
    data = {"email": "test@user.com", "not_hashed_password": "test"}
    response = client.post("/v1/create-user", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "test@user.com"
    # TODO add user with same email check 400
