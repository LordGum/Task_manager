def test_get_all_todos(client, db_session):
    client.post("/todos/", json={"title": "Task 1", "description": "Desc 1"})
    client.post("/todos/", json={"title": "Task 2", "description": "Desc 2"})

    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"


def test_get_todo_by_id(client, sample_todo):
    response = client.get(f"/todos/{sample_todo.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_todo.id
    assert data["title"] == "Test Task"
    assert data["priority"] == 5


def test_get_nonexistent_todo(client):
    response = client.get("/todos/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_top_priority_todos(client, db_session):
    client.post("/todos/", json={"title": "Low", "description": "", "priority": 1})
    client.post("/todos/", json={"title": "High", "description": "", "priority": 10})
    client.post("/todos/", json={"title": "Medium", "description": "", "priority": 5})

    response = client.get("/todos/top/2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "High"
    assert data[1]["title"] == "Medium"


def test_get_todos_with_sorting(client, db_session):
    client.post("/todos/", json={"title": "Zebra", "description": "", "status": "active"})
    client.post("/todos/", json={"title": "Apple", "description": "", "status": "done"})

    response = client.get("/todos/?sort_by=title")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["title"] == "Apple"
    assert data[1]["title"] == "Zebra"


def test_get_todos_with_pagination(client, db_session):
    for i in range(5):
        client.post("/todos/", json={"title": f"Task {i}", "description": ""})

    response = client.get("/todos/?skip=2&limit=2")
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 2"
    assert data[1]["title"] == "Task 3"