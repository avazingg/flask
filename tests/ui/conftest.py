"""file with fixtures and configs"""
import os
from datetime import datetime
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tests.ui.endpoints.register_page import RegisterPage
from settings import url
from app import app, db

import allure

@pytest.fixture
def driver():
    """"fixture for quick driver access"""
    options = Options()
    options.add_argument("--start-maximized")
    service = Service(ChromeDriverManager().install())
    config_driver = webdriver.Chrome(service=service, options=options)
    yield config_driver
    config_driver.quit()

@pytest.fixture
def register_user(driver):
    """fixture for quick registration"""
    register_page = RegisterPage(driver)
    register_page.open_url(f"{url}register")
    register_page.enter_username("username")
    register_page.enter_password("password")
    register_page.click_register()
    return {
        "username": "username",
        "password": "password"
    }


@pytest.fixture
def registration_alert(driver):
    """fixture for get registration alert"""
    register_page = RegisterPage(driver)
    register_page.open_url(f"{url}register")
    def get_alert(username, password, type_of_alert="error"):
        if type_of_alert == "error":
            type_of_alert= register_page.ERROR_ALERT
        else:
            type_of_alert = register_page.SUCCESS_ALERT
        register_page.enter_username(username)
        register_page.enter_password(password)
        register_page.click_register()
        return register_page.get_alert_message(type_of_alert)

    return get_alert

@pytest.fixture
def db_session():
    """fixture for interaction with DB"""
    with app.app_context():
        session = db.session
        yield session
        session.rollback()
        session.close()

def save_screenshot(driver, folder_path='screenshots',\
                    filename_prefix='screenshot', attach_to_allure=True):
    """"method for making screenshot"""
    os.makedirs(folder_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{filename_prefix}_{timestamp}.png"
    filepath = os.path.join(folder_path, filename)
    driver.save_screenshot(filepath)
    if attach_to_allure:
        with open(filepath, "rb") as image_file:
            allure.attach(image_file.read(), name=filename_prefix,\
                          attachment_type=allure.attachment_type.PNG)

    return filepath
