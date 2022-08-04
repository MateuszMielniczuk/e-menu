import logging

CREATE_DATA = {"name": "Menu name", "description": "Menu description"}


def test_create_menu(client, user_token_header):
    logging.info("Test menu card create endpoint")
    response = client.post("/v1/menu_card", json=CREATE_DATA, headers=user_token_header)
    assert response.status_code == 201


def test_create_menu_not_unique_name(client, user_token_header):
    response = client.post("/v1/menu_card", json=CREATE_DATA, headers=user_token_header)
    assert response.status_code == 405
    assert response.json()["detail"] == "Menu card name: 'Menu name' exists. Name must be unique!"


def test_get_menu_detail(client):
    response = client.get("/v1/menu_card/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Menu name"
    assert response.json()["description"] == "Menu description"


def test_menu_detail_id_not_found(client):
    response = client.get("/v1/menu_card/111")
    assert response.status_code == 404
    assert response.json()["detail"] == "Menu with ID: '111' not found in database"


UPDATE_DATA = {"name": "Updated name", "description": "Updated description"}


def test_update_menu(client, user_token_header):
    response = client.put("/v1/menu_card/1", json=UPDATE_DATA, headers=user_token_header)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated name"
    assert response.json()["description"] == "Updated description"


def test_update_menu_id_not_found(client, user_token_header):
    response = client.put("/v1/menu_card/112", json=UPDATE_DATA, headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Menu with ID: '112' not found in database"


def test_update_menu_not_unique_name(client, user_token_header):
    response = client.put("/v1/menu_card/1", json=UPDATE_DATA, headers=user_token_header)
    assert response.status_code == 405
    assert response.json()["detail"] == "Menu card name: 'Updated name' exists. Name must be unique!"


def test_add_dish_to_menu(client, user_token_header):
    data = {"name": "Dish name", "description": "Dish description ...", "is_vegan": True}
    client.post("/v1/dish", json=data, headers=user_token_header)
    response = client.post("/v1/menu_card/1/dish=1", headers=user_token_header)
    assert response.status_code == 201
    assert response.json() == "Dish successfully added to menu"


def test_get_menus(client):
    response = client.get("/v1/menu_card")
    assert response.status_code == 200
    content = response.json()[0]
    assert content["name"] == "Updated name"


def test_add_dish_menu_not_found(client, user_token_header):
    response = client.post("/v1/menu_card/111/dish=1", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Menu with ID: '111' not found in database"


def test_add_dish_dish_not_found(client, user_token_header):
    response = client.post("/v1/menu_card/1/dish=123", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Dish with ID: 123 not found in database"


def test_add_dish_already_exists(client, user_token_header):
    response = client.post("/v1/menu_card/1/dish=1", headers=user_token_header)
    assert response.status_code == 405
    assert response.json()["detail"] == "Dish already in menu!"


def test_delete_dish_menu_not_found(client, user_token_header):
    response = client.delete("/v1/menu_card/111/dish=1", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Menu with ID: '111' not found in database"


def test_delete_dish_dish_not_found(client, user_token_header):
    response = client.delete("/v1/menu_card/1/dish=123", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Dish with ID: 123 not found in database"


def test_delete_dish_not_in_junction(client, user_token_header):
    data = {"name": "Dish name 2", "description": "Dish description 2", "is_vegan": True}
    client.post("/v1/dish", json=data, headers=user_token_header)
    response = client.delete("/v1/menu_card/1/dish=2", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Dish not found in selected menu!"


def test_delete_dish_from_menu(client, user_token_header):
    response = client.delete("/v1/menu_card/1/dish=1", headers=user_token_header)
    assert response.status_code == 204


def test_delete_menu_not_found(client, user_token_header):
    response = client.delete("/v1/menu_card/113", headers=user_token_header)
    assert response.status_code == 404
    assert response.json()["detail"] == "Menu with ID: '113' not found in database"


def test_delete_menu(client, user_token_header):
    response = client.delete("v1/menu_card/1", headers=user_token_header)
    assert response.status_code == 204
