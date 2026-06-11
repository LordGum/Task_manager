# Todo App with Docker
Простое Todo-приложение на FastAPI + MySQL + Docker.


## Запуск
docker-compose up -d


## API
Метод	       URL	             Описание \
POST	       /todos/	         Создать задачу \
GET	         /todos/	         Получить все задачи \
GET	         /todos/{id}	     Получить задачу по ID \
PUT	         /todos/{id}	     Обновить задачу \
DELETE	     /todos/{id}	     Удалить задачу \


## Примеры
#### Создать задачу
curl -X POST http://localhost:8000/todos/ -H "Content-Type: application/json" -d '{"title":"Купить молоко","description":"сходить в магазин"}'

#### Получить все задачи
curl http://localhost:8000/todos/

#### Обновить статус
curl -X PUT http://localhost:8000/todos/1 -H "Content-Type: application/json" -d '{"status":"готово"}'

#### Удалить задачу
curl -X DELETE http://localhost:8000/todos/1



