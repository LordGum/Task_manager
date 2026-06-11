from locust import HttpUser, task, between
import random
import string

class TodoUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.todo_id = None

    @task(3)
    def create_todo(self):
        random_title = ''.join(random.choices(string.ascii_letters, k=10))
        response = self.client.post("/todos/", json={
            "title": f"Load test {random_title}",
            "description": "Testing performance",
            "priority": random.randint(0, 10)
        })
        if response.status_code == 200:
            self.todo_id = response.json()["id"]

    @task(2)
    def get_all_todos(self):
        self.client.get("/todos/?skip=0&limit=50")

    @task(2)
    def search_todos(self):
        search_terms = ["test", "load", "python", "todo"]
        term = random.choice(search_terms)
        self.client.get(f"/todos/search/?q={term}")

    @task(1)
    def get_top_priority(self):
        n = random.randint(1, 10)
        self.client.get(f"/todos/top/{n}")

    @task(1)
    def update_todo(self):
        if self.todo_id:
            self.client.put(f"/todos/{self.todo_id}", json={
                "status": random.choice(["в ожидании", "выполнено", "в процессе"])
            })

    @task(1)
    def delete_todo(self):
        if self.todo_id:
            self.client.delete(f"/todos/{self.todo_id}")
            self.todo_id = None