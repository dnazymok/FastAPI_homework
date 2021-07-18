from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

valid_data = {
    "name": "Geralt",
    "username": "Geralt",
    "email": "Geralt@example.com",
    "phone": "88005553535"
}

invalid_data = {
    "name": 1488,
    "username": [123, 125],
    "email": "BlaBla",
    "phone": [123, 'bla']
}


def test_user_list():
    response = client.get("/users/")
    assert response.status_code == 200
    response_data = response.json()[0]
    assert "id" in response_data
    assert "name" in response_data
    assert "username" in response_data
    assert "email" in response_data
    assert "phone" in response_data


def test_create_user():
    response = client.post("/users/", json=valid_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == 11
    assert response_data["name"] == "Geralt"
    assert response_data["username"] == "Geralt"
    assert response_data["email"] == "Geralt@example.com"
    assert response_data["phone"] == "88005553535"


def test_invalid_user_create():
    response = client.post("/users/", json=invalid_data)
    assert response.status_code == 422
