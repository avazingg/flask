import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tests.ui.endpoints.login_page import LoginPage
from tests.ui.payload import payload

import pytest
import allure


@allure.feature("UI Тест")
@allure.story("Тест авторизации существующего пользователя")
@allure.severity(allure.severity_level.BLOCKER)
def test_login(driver):
    login_page = LoginPage(driver)
    login_page.login_procedure(payload.valid_created_payload["username"], payload.valid_created_payload["password"])
    assert "Вы успешно вошли в систему" in login_page.get_alert_message(login_page.SUCCESS_ALERT)
