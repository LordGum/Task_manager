def test_create_todo_empty_title(client):
    response = client.post("/todos/", json={
        "title": "",
        "description": "Some description"
    })
    assert response.status_code in [200, 422]

def test_create_todo_invalid_priority_type(client):
    response = client.post("/todos/", json={
        "title": "Test",
        "description": "Test",
        "priority": "not a number"
    })
    assert response.status_code == 422

def test_create_todo_extra_fields(client):
    response = client.post("/todos/", json={
        "title": "Test",
        "description": "Test",
        "extra_field": "should be ignored"
    })
    assert response.status_code == 200

def test_get_todos_invalid_sort_by(client):
    response = client.get("/todos/?sort_by=invalid_field")
    assert response.status_code == 422