def test_update_todo_success(client, sample_todo):
    response = client.put(f"/todos/{sample_todo.id}", json={
        "title": "Updated Title",
        "priority": 99
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["priority"] == 99
    assert data["description"] == "Test Description"


def test_update_partial_fields(client, sample_todo):
    response = client.put(f"/todos/{sample_todo.id}", json={
        "status": "выполнено"
    })

    data = response.json()
    assert data["status"] == "выполнено"
    assert data["title"] == "Test Task"


def test_update_nonexistent_todo(client):
    response = client.put("/todos/99999", json={"title": "New Title"})
    assert response.status_code == 404


def test_delete_todo_success(client, sample_todo):
    response = client.delete(f"/todos/{sample_todo.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully"

    get_response = client.get(f"/todos/{sample_todo.id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_todo(client):
    response = client.delete("/todos/99999")
    assert response.status_code == 404