def test_create_todo_success(client):
    response = client.post("/todos/", json={
        "title": "Learn Testing",
        "description": "Write comprehensive tests",
        "status": "в ожидании",
        "priority": 10
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Learn Testing"
    assert data["description"] == "Write comprehensive tests"
    assert data["status"] == "в ожидании"
    assert data["priority"] == 10
    assert "id" in data
    assert "created_at" in data


def test_create_todo_without_optional_fields(client):
    response = client.post("/todos/", json={
        "title": "Minimal Task",
        "description": "Only required fields"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Minimal Task"
    assert data["status"] == "в ожидании"
    assert data["priority"] == 0