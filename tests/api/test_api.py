import os
import pytest
import allure
import requests
import psycopg2


# Параметры подключения к БД (из переменных окружения или дефолтные значения)
DB_PARAMS = {
    'dbname': os.environ.get('POSTGRES_DB', 'taskmanager'),
    'user': os.environ.get('POSTGRES_USER', 'postgres'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
    'host': os.environ.get('POSTGRES_HOST', 'db'),
    'port': os.environ.get('POSTGRES_PORT', '5432')
}

# URL API-сервера
BASE_URL = "http://web:5000/api"

# Данные тестового пользователя
TEST_USER = {"username": "testuser1", "password": "testpass"}


@pytest.fixture(scope="function")
def db_connection():
    """Фикстура для подключения к БД"""
    print("🔌 Подключение к БД...")
    conn = psycopg2.connect(**DB_PARAMS)  # Устанавливаем соединение с БД
    yield conn  # Передаем соединение в тест
    conn.close()  # Закрываем соединение после теста
    print("🔌 Соединение с БД закрыто.")


@pytest.fixture(scope="function")
def session(db_connection):
    """Фикстура для HTTP-сессии с авторизацией. Если пользователь не найден, создаем его"""
    session = requests.Session()

    # Проверяем, есть ли пользователь в базе
    cursor = db_connection.cursor()
    print(f"🔍 Проверка пользователя {TEST_USER['username']} в БД...")
    cursor.execute('SELECT id FROM "user" WHERE username = %s', (TEST_USER["username"],))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        print(f"⚠️ Пользователь {TEST_USER['username']} не найден в БД. Создаю нового пользователя...")

        # Создаем пользователя через API
        register_response = session.post(f"{BASE_URL}/register", json=TEST_USER)
        assert register_response.status_code == 201, f"❌ Ошибка при создании пользователя: {register_response.text}"

        print(f"✅ Пользователь {TEST_USER['username']} успешно создан!")

    # Выполняем авторизацию
    print(f"🔑 Авторизация в API для пользователя: {TEST_USER['username']}")
    login_response = session.post(f"{BASE_URL}/login", json=TEST_USER)

    assert login_response.status_code == 200, f"❌ Ошибка входа в систему: {login_response.text}"
    print("✅ Успешный вход в систему!")

    return session  # Возвращаем авторизованную сессию


@allure.feature("API Тест")
@allure.story("Полный цикл создания задачи")
def test_full_task_creation(db_connection, session):
    """Тест проверяет, что пользователь существует, успешно логинится, создает задачу и она есть в БД"""

    with allure.step("Получение ID пользователя из БД"):
        cursor = db_connection.cursor()
        cursor.execute('SELECT id FROM "user" WHERE username = %s', (TEST_USER["username"],))
        user = cursor.fetchone()
        cursor.close()
        assert user is not None, f"❌ Пользователь {TEST_USER['username']} не найден в БД!"
        user_id = user[0]
        print(f"✅ Пользователь найден в БД: ID {user_id}")

    with allure.step("Создание новой задачи через API"):
        task_data = {
            "title": "Тестовая задача",
            "description": "Описание тестовой задачи",
            "completed": False
        }
        print("📩 Отправка запроса на создание задачи...")
        create_task_response = session.post(f"{BASE_URL}/tasks", json=task_data)
        print(f"📩 Ответ API на создание задачи: {create_task_response.status_code}")

        assert create_task_response.status_code == 201, f"❌ Ошибка при создании задачи: {create_task_response.text}"
        created_task = create_task_response.json()
        assert "id" in created_task, "❌ Ответ API не содержит 'id' созданной задачи!"
        task_id = created_task["id"]
        print(f"✅ Задача успешно создана! ID: {task_id}")

    with allure.step("Проверка, что задача записана в БД"):
        print(f"🔍 Проверка задачи {task_id} в БД...")
        cursor = db_connection.cursor()
        cursor.execute("SELECT id, title, description FROM task WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        cursor.close()
        assert task is not None, f"❌ Задача с ID {task_id} не найдена в БД!"
        print(f"✅ Задача найдена в БД: {task}")
