"""file with fixtures and configs"""
import pytest
import psycopg2
import requests

from db_interaction import DatabaseManager
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.register_user import RegisterUser
from tests.api.payload.payload import api_payload
from tests.api.test_api import DB_PARAMS


@pytest.fixture(scope="function")
def db_connection():
    """Подключение к базе данных PostgreSQL для выполнения тестов."""
    conn = psycopg2.connect(**DB_PARAMS)
    yield conn
    conn.close()

@pytest.fixture
def session():
    """Создает и возвращает сессию для тестов API."""
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture
def register_login_user(session):
    """Фикстура для регистрации и логина пользователя через API."""
    db = DatabaseManager()
    db.restart_whole_db()

    user_data = api_payload

    register = RegisterUser()
    response = register.register_user(user_data, session)

    login = LoginUser()
    login_response = login.login_user({
        "username": user_data["username"],
        "password": user_data["password"]
    }, session=session)

    return {
        "username": user_data["username"],
        "password": user_data["password"],
        "response": response,
        "login_response": login_response,
        "user_id": login_response.get("user_id"),
        "message": login_response.get("message"),
    }
