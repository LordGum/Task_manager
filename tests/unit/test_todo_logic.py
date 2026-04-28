import pytest
from app.models import Todo

def test_filter_by_priority_logic():
    todos = [
        Todo(priority=1, title="Low"),
        Todo(priority=5, title="High"),
        Todo(priority=3, title="Medium"),
    ]
    sorted_todos = sorted(todos, key=lambda x: x.priority, reverse=True)
    assert sorted_todos[0].priority == 5
    assert sorted_todos[0].title == "High"
    assert sorted_todos[1].priority == 3
    assert sorted_todos[2].priority == 1


def test_search_logic():
    todos = [
        {"title": "Buy milk", "description": "Get from store"},
        {"title": "Python project", "description": "Write tests"},
        {"title": "Read book", "description": "Python learning"},
    ]

    def search(q, todos_list):
        q_lower = q.lower()
        return [t for t in todos_list
                if q_lower in t["title"].lower() or q_lower in t["description"].lower()]

    results = search("python", todos)
    assert len(results) == 2
    assert results[0]["title"] == "Python project"
    assert results[1]["title"] == "Read book"

    results = search("learning", todos)
    assert len(results) == 1
    assert results[0]["title"] == "Read book"

    results = search("xyz", todos)
    assert len(results) == 0


def test_sorting_logic():
    todos = [
        {"title": "Buy milk", "status": "в ожидании", "created_at": "2024-01-01"},
        {"title": "Python project", "status": "выполнено", "created_at": "2024-01-02"},
        {"title": "Read book", "status": "в процессе", "created_at": "2024-01-03"},
    ]

    sorted_by_title = sorted(todos, key=lambda x: x["title"])
    assert sorted_by_title[0]["title"] == "Buy milk"
    assert sorted_by_title[1]["title"] == "Python project"
    assert sorted_by_title[2]["title"] == "Read book"

    sorted_by_status = sorted(todos, key=lambda x: x["status"])
    assert sorted_by_status[0]["status"] == "в ожидании"
    assert sorted_by_status[1]["status"] == "в процессе"
    assert sorted_by_status[2]["status"] == "выполнено"

    sorted_by_date = sorted(todos, key=lambda x: x["created_at"])
    assert sorted_by_date[0]["created_at"] == "2024-01-01"
    assert sorted_by_date[1]["created_at"] == "2024-01-02"
    assert sorted_by_date[2]["created_at"] == "2024-01-03"