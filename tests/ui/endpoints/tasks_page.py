from selenium.webdriver.common.by import By

from tests.ui.endpoints.base_page import BasePage

class TasksPage(BasePage):
    CREATE_TASK_BUTTON = (By.CSS_SELECTOR, "[data-testid='create-task-button']")

    def change_task_status(self, taskid = 1):
        element = (By.CSS_SELECTOR, f"[data-testid='toggle-button-{taskid}']")
        self.click_element(element)

    def view_task(self, taskid=1):
        element = (By.CSS_SELECTOR, f"[data-testid='view-task-button-{taskid}']")
        self.click_element(element)

    def edit_task(self, taskid):
        element = (By.CSS_SELECTOR, f"[data-testid='edit-task-button-{taskid}']")
        self.click_element(element)

    def delete_task(self, taskid):
        element = (By.CSS_SELECTOR, f"[data-testid='delete-task-button-{taskid}']")
        self.click_element(element)

    def create_new_task(self, name, description=""):
        self.click_element(self.CREATE_TASK_BUTTON)
        self.enter_text(self.TASK_NAME_INPUT, name)
        self.enter_text(self.TASK_NAME_INPUT, description)
        self.click_element(self.SUBMIT_TASK_BUTTON)

    def get_task_name(self, taskid):
        task_title = (By.CSS_SELECTOR, f"[data-testid='task-title-{taskid}']")
        element = self.find_element(task_title)
        return element.text
