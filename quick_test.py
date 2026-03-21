import requests
import time

BASE = "http://127.0.0.1:8000"
time.sleep(2)

tasks = [
    ("Купить молоко", "Купить 2 литра", "в ожидании", 9),
    ("Сделать отчет", "Отчет для начальника", "в работе", 10),
    ("Позвонить маме", "Не забыть", "в ожидании", 7),
]

for title, desc, status, priority in tasks:
    requests.post(f"{BASE}/todos/", json={
        "title": title,
        "description": desc,
        "status": status,
        "priority": priority
    })

print("Создано 3 задачи")
print("\nВсе задачи:", requests.get(f"{BASE}/todos/").json())
print("\nТоп-2:", requests.get(f"{BASE}/todos/top/2").json())
print("\nПоиск 'отчет':", requests.get(f"{BASE}/todos/search/", params={"q": "отчет"}).json())