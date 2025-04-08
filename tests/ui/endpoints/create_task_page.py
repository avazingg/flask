from selenium.webdriver.common.by import By
from tests.ui.endpoints.base_page import BasePage
from tests.ui.payload import payload

class CreateTaskPage(BasePage):
    TASK_NAME_INPUT = (By.CSS_SELECTOR, "[data-testid='title-input']")
    TASK_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='description-input']")
    SUBMIT_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='submit-button']")
    CANCEL_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='cancel-button']")
    ERROR_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-danger']")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "[data-testid='flash-message-success']")

    def create_new_task(self, name, description=""):
        self.enter_text(self.TASK_NAME_INPUT, name)
        self.enter_text(self.TASK_DESCRIPTION_INPUT, description)
        self.click_element(self.SUBMIT_TASK_BUTTON)