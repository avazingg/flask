from tests.api.endpoints.register_user import RegisterUser
from db_interaction import DatabaseManager

import allure


@allure.feature("API Тесты")
@allure.story("Регистрация пользователя")
def test_register(session):
    test_user = {
        "username": "apiuser1",
        "password": "apiuser"
    }

    with allure.step("Перезапускаем базу данных"):
        db = DatabaseManager()
        db.restart_whole_db()

    with allure.step("Регистрируем нового пользователя"):
        register = RegisterUser()
        response_json = register.register_user(test_user, session)

    with allure.step("Проверяем успешную регистрацию"):
        register.check_response_is_201()

    with allure.step("Проверяем сообщение об успешной регистрации"):
        assert "Регистрация успешна" in response_json["message"],\
            "получено другое сообщение"