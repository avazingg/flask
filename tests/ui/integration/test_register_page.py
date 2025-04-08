import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from tests.ui.conftest import registration_alert
from tests.ui.endpoints.base_page import BasePage
from tests.ui.endpoints.register_page import RegisterPage
from tests.ui.endpoints.login_page import LoginPage
from tests.ui.payload import payload
from settings import url


import pytest
import allure

@allure.feature("UI Тест")
@allure.story("Тест регистрации уже зарегестрированного юзера")
@allure.severity(allure.severity_level.BLOCKER)
def test_registration_of_existing_user(driver):
    """Тест проверяет, что пользователь, который уже зарегистрирован, пытается ввести те же данные при регистрации"""
    register_page = RegisterPage(driver)
    with allure.step("Открываем страницу регистрации"):
        register_page.open_url(f"{url}/register")

    with allure.step("Вводим данные уже зарегестрированного пользователя"):
        register_page.enter_username(payload.valid_created_payload["username"])
        register_page.enter_password(payload.valid_created_payload["password"])

    with allure.step("Нажимаем 'Зарегистрироваться'"):
        register_page.click_element(register_page.REGISTER_BUTTON)

    # Делаем скриншот и сохраняем его в папку screenshots
    screenshots_dir = os.path.join(os.getcwd(), "screenshots")
    screenshot_path = os.path.join(screenshots_dir,
                                   "screenshot_existing_user_registration_test.png")
    driver.save_screenshot(screenshot_path)

    assert "Пользователь с таким именем уже существует" in register_page.get_alert_message(register_page.ERROR_ALERT),\
        "Пользователь уже существует, мы должны получить информацию об этом"

@allure.feature("UI Тест")
@allure.story("Тест регистрации уже зарегестрированного юзера")
@allure.severity(allure.severity_level.BLOCKER)
def test_registration_of_existing_user(driver, registration_alert):
    error_text = registration_alert("username", "password")
    assert "Пользователь с таким именем уже существует" in error_text, f"Ожидали: 1, но получили: {error_text}"

invalid_cridentials = [
   ("name", "name", "Пароль должен содержать не менее 6 символов"),
    ("1", "namename", "Имя пользователя должно содержать не менее 3 символов"),
]
@pytest.mark.parametrize("username, password, expected", invalid_cridentials)
@allure.feature("UI Тест")
@allure.story("Тест регистрации пользователя со паролем короче 6 символов")
@allure.severity(allure.severity_level.NORMAL)
def test_registration_with_too_short_password(driver, registration_alert, username, password, expected):
    error_text = registration_alert(username, password)
    assert expected in error_text, f"Ожидали: {expected}, но получили: {error_text}"