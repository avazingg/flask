from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from settings import url

class BasePage():
    def __init__(self, driver):
        self.driver = driver

    ERROR_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-danger']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-success']")

    def open_url(self, url):
        self.driver.get(url)

    def open_start_page(self):
        self.driver.get(url)

    def find_element(self, locator, timeout = 10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except TimeoutException:
            return None

    def click_element(self, locator, timeout = 10):
        self.find_element(locator, timeout).click()

    def enter_text(self, locator, text, timeout = 10):
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def get_alert_message(self,locator, timeout=10):
       return self.find_element(locator, timeout).get_attribute("textContent")

    # def is_element_present(self, locator, timeout=5):
    #     try:
    #         WebDriverWait(self, timeout).until(EC.presence_of_element_located(locator))
    #         return True
    #     except TimeoutException:
    #         return False