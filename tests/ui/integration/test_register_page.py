"""Тестируем страницу регистрации"""
import pytest
import allure
from tests.ui.conftest import save_screenshot

@allure.feature("UI Тест")
@allure.story("Тест регистрации уже зарегестрированного юзера")
@allure.severity(allure.severity_level.BLOCKER)
def test_registration_of_existing_user(driver, register_user, registration_alert):
    """"Тест регистрации уже зарегестрированного юзера"""
    creds = register_user
    error_text = registration_alert(creds["username"], creds["password"])
    save_screenshot(driver, folder_path="screenshots/UI/module",\
                    filename_prefix="alreadey_existing_user")
    assert "Пользователь с таким именем уже существует" in\
           error_text, f"Ожидали: 1, но получили: {error_text}"


invalid_cridentials = [
   ("name", "name", "Пароль должен содержать не менее 6 символов"),
    ("1", "namename", "Имя пользователя должно содержать не менее 3 символов"),
]

@pytest.mark.parametrize("username, password, expected", invalid_cridentials)
@allure.feature("UI Тест")
@allure.story("Тест регистрации пользователя с невалидными данными")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_with_too_short_credentials(driver, registration_alert,\
                                                 username, password, expected):
    """"Тест регистрации пользователя с невалидными данными"""
    error_text = registration_alert(username, password)
    save_screenshot(driver, folder_path="screenshots/UI/module", filename_prefix=expected)
    assert expected in error_text, f"Ожидали: {expected}, но получили: {error_text}"
