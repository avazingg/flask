from selenium.webdriver.common.by import By

from tests.ui.endpoints.base_page import BasePage

class ViewTask(BasePage):
    BACK_BUTTON = (By.CSS_SELECTOR, "[data-testid='back-button']")
    TOGGLE_STATUS_BUTTON = (By.CSS_SELECTOR, "[data-testid='toggle-status-button']")
    EDIT_BUTTON = (By.CSS_SELECTOR, "[data-testid='edit-button']")
    DELETE_BUTTON = (By.CSS_SELECTOR, "[data-testid='delete-button']")
