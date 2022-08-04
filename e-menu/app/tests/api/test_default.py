import logging


def test_default_endpoint(client):
    logging.info("Test default endpoint")
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to eMenu app!"
