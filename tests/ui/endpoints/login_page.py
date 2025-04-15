from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tests.ui.endpoints.base_page import BasePage
from tests.ui.payload import payload
from  settings import url

class LoginPage(BasePage):
    USERNAME_INPUT = (By.CSS_SELECTOR, "[data-testid='username-input']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-testid='password-input']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='login-button']")
    REGISTER_LINK = (By.CSS_SELECTOR, "[data-testid='register-link']")
    ERROR_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-danger']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-success']")
    LOGIN_LINK = (By.CSS_SELECTOR, "[data-testid='nav-login']")

    def enter_username(self, username):
        self.enter_text(locator=self.USERNAME_INPUT, text=username)

    def enter_password (self, password):
        self.enter_text(locator=self.PASSWORD_INPUT, text=password)

    def click_login(self):
        self.click_element(self.LOGIN_BUTTON)

    def click_register_link(self):
        self.click_element(self.REGISTER_LINK)

    def login_procedure(self, username, password):
        self.open_url(f"{url}login")
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
