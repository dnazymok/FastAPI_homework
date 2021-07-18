from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

valid_data = {
    "userId": 1,
    "title": "Some Title",
    "body": "Some Body"
}

invalid_data = {
  "userId": "1",
  "title": 123,
  "body": [1, 2, 3]
}

def test_post_list():
    response = client.get("/posts")
    assert response.status_code == 200
    response_data = response.json()[0]
    assert "id" in response_data
    assert "title" in response_data
    assert "body" in response_data
    assert "author" in response_data


def test_post_create():
    response = client.post("/posts/", json=valid_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["id"] == 101
    assert response_data["title"] == "Some Title"
    assert response_data["body"] == "Some Body"
    assert response_data["author"]["id"] == 1


def test_invalid_post_create():
    response = client.post("/posts/", json=invalid_data)
    assert response.status_code == 422


def test_detail_post():
    response = client.get("/posts/1")
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert "title" in response_data
    assert "body" in response_data
    assert "author" in response_data
    assert "comments" in response_data


def test_update_post():
    valid_data = {"title": "string", "body": "string"}
    response = client.patch("/posts/3", json=valid_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "string"
    assert response_data["body"] == "string"
    assert "id" in response_data
