#!/bin/bash

# Установка зависимостей для тестирования
pip install pytest pytest-cov httpx locust pytest-mock

# Запуск юнит и функциональных тестов с покрытием
echo "Running unit and functional tests..."
coverage run -m pytest tests/unit tests/functional -v
coverage report -m

# Проверка минимального покрытия (например, 70%)
coverage report | grep -q "TOTAL.*70%" && echo "✅ Coverage OK" || echo "⚠️ Coverage below 70%"

# Запуск нагрузочного тестирования (без интерфейса, 10 секунд)
echo "Running load tests for 10 seconds..."
locust -f tests/load/locustfile.py --headless --users 10 --spawn-rate 2 --run-time 10s --host=http://localhost:8000

echo "Tests completed!"