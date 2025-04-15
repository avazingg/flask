"""Unit tests for user login API endpoint."""
import allure

@allure.feature("API Тесты")
@allure.story("Авторизация пользователя")
def test_login(register_login_user):
    """Тестирует успешную авторизацию через API."""
    user_id = register_login_user["user_id"]
    login_response = register_login_user["login_response"]

    with allure.step("Проверяем успешный вход в систему"):
        assert login_response["message"] == "Вы успешно вошли в систему", \
            f"Expected message 'Вы успешно вошли в систему' but got {login_response['message']}"

    with allure.step("Проверяем user_id"):
        assert user_id == login_response["user_id"], \
            f"Expected user_id {user_id} but got {login_response['user_id']}"

    with allure.step("Проверяем username"):
        assert register_login_user["username"] == login_response["username"], \
            f"Expected username {register_login_user['username']}\
             but got {login_response['username']}"
