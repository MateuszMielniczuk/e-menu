import logging


def test_create_dish(client, user_token_header):
    logging.info("Test dish create endpoint")
    data = {"name": "Dish name", "description": "Dish description ...", "is_vegan": True}
    response = client.post("/v1/dish", json=data, headers=user_token_header)
    assert response.status_code == 201


def test_show_all_dishes(client):
    logging.info("Test show all dishes endpoint")
    response = client.get("v1/dish")
    assert response.status_code == 200
    content = response.json()[0]
    assert content["name"] == "Dish name"
    assert content["description"] == "Dish description ..."
    assert content["is_vegan"] is True
    assert content["id"] == 1


def test_user_update_not_found(client, user_token_header):
    data = {"name": "Updated name", "description": "Updated description", "is_vegan": False}
    response = client.put("/v1/dish/2", json=data, headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Dish with ID: 2 not found in database"


def test_update_dish(client, user_token_header):
    logging.info("Test update item endpoint")
    data = {"name": "Updated name", "description": "Updated description", "is_vegan": False}
    response = client.put("/v1/dish/1", json=data, headers=user_token_header)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == "Updated name"
    assert content["description"] == "Updated description"
    assert content["is_vegan"] is False


def test_user_delete_not_found(client, user_token_header):
    response = client.delete("/v1/dish/3", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Dish with ID: 3 not found in database"


def test_delete_dish(client, user_token_header):
    response = client.delete("/v1/dish/1", headers=user_token_header)
    assert response.status_code == 204
