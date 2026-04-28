def test_search_todos_by_title(client, db_session):
    client.post("/todos/", json={"title": "Python programming", "description": "Learn Python"})
    client.post("/todos/", json={"title": "Java basics", "description": "Learn Java"})

    response = client.get("/todos/search/?q=python")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Python programming"


def test_search_todos_by_description(client, db_session):
    client.post("/todos/", json={
        "title": "Task 1",
        "description": "This contains the keyword TEST"
    })

    response = client.get("/todos/search/?q=TEST")
    data = response.json()
    assert len(data) == 1
    assert data[0]["description"] == "This contains the keyword TEST"


def test_search_no_results(client):
    response = client.get("/todos/search/?q=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0