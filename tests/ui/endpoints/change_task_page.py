from selenium.webdriver.common.by import By
from tests.ui.endpoints.base_page import BasePage


class ChangeTaskPage(BasePage):
    TASK_NAME_INPUT = (By.CSS_SELECTOR, "[data-testid='title-input']")
    TASK_DESCRIPTION_INPUT = (By.CSS_SELECTOR, "[data-testid='description-input']")
    SUBMIT_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='submit-button']")
    CANCEL_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='cancel-button']")
    CHANGE_STATUS_CHECKBOX = (By.CSS_SELECTOR, "[data-testid='completed-checkbox']")

    def update_task(self, name, description=""):
        self.enter_text(self.TASK_NAME_INPUT, name)
        self.enter_text(self.TASK_DESCRIPTION_INPUT, description)
        self.click_element(self.SUBMIT_TASK_BUTTON)

    def click_checkbox(self):
        self.click_element(self.CHANGE_STATUS_CHECKBOX)
        self.click_element(self.SUBMIT_TASK_BUTTON)