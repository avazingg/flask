from dill import settings
from selenium.webdriver.common.by import By
from tests.ui.endpoints.base_page import BasePage

from tests.ui.payload import payload
from settings import url

class RegisterPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-testid='username-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='password-input']")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "[data-testid='register-button']")
    ERROR_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-danger']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-success']")
    LOGIN_LINK = (By.CSS_SELECTOR, "[data-testid='nav-login']")
    REGISTER_LINK = (By.CSS_SELECTOR, "[data-testid='nav-register']")

    def enter_username(self, username):
        self.enter_text(self.USERNAME_INPUT, username)

    def enter_password (self, password):
        self.enter_text(self.PASSWORD_INPUT, password)

    def click_register(self):
        self.click_element(self.REGISTER_BUTTON)

    def registration_procedure(self, username, password):
        self.open_url(f"{url}register")
        self.enter_username(username)
        self.enter_password(password)
        self.click_register()

    def click_login_link(self):
        self.click_element(self.LOGIN_LINK)

    def click_register_link(self):
        self.click_element(self.REGISTER_LINK)