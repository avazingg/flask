from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.ui.endpoints.base_page import BasePage
from tests.ui.payload import payload

# class ModalWindow(BasePage):
#     def cancel_delete(self, taskid):
#         cancel_button = (By.CSS_SELECTOR, f"[data-testid='delete-modal-cancel-{taskid}']")
#         element = self.find_element(cancel_button)
#         self.click_element(element)
#
#     def submit_delete(self, taskid):
#         delete_button = (By.CSS_SELECTOR, f"[data-testid='delete-confirm-button-{taskid}']")
#         element = self.find_element(delete_button)
#         self.click_element(element)
class ModalWindow(BasePage):
    def cancel_delete(self, taskid):
        cancel_button = (By.CSS_SELECTOR, f"[data-testid='delete-modal-cancel-{taskid}']")

        # Ждём появления кнопки "Отмена"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(cancel_button)
        )

        # Кликаем по кнопке
        self.driver.find_element(*cancel_button).click()

    def submit_delete(self, taskid):
        modal_locator = (By.CSS_SELECTOR, f"[data-testid='delete-modal-{taskid}']")
        delete_button = (By.CSS_SELECTOR, f"[data-testid='delete-confirm-button-{taskid}']")

        # Ждём, пока появится модальное окно
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(modal_locator)
        )

        # Ждём, пока кнопка "Удалить" станет кликабельной
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(delete_button)
        )

        # Кликаем по кнопке
        self.driver.find_element(*delete_button).click()