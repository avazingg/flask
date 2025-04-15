"""UI Тестируем полный жизненный цикл приложения для задачи."""

import allure

from tests.ui.endpoints.login_page import LoginPage
from tests.ui.endpoints.modal_delete import ModalWindow
from tests.ui.endpoints.register_page import RegisterPage
from tests.ui.endpoints.tasks_page import TasksPage
from tests.ui.endpoints.create_task_page import CreateTaskPage
from tests.ui.endpoints.view_task_page import ViewTask
from tests.ui.endpoints.change_task_page import ChangeTaskPage
from tests.ui.payload import payload
from tests.ui.conftest import save_screenshot
from db_interaction import DatabaseManager

# pylint: disable=too-many-statements
@allure.feature("UI Тест")
@allure.story("Полный цикл создания задачи")
def test_e2e_ui_test(driver):
    """Тест проверяет полный жизненный цикл приложения"""
    # db = DatabaseManager()
    # db.restart_whole_db()
    with allure.step("Открываем домашнюю страницу"):
        register_page = RegisterPage(driver)
        login_page = LoginPage(driver)
        login_page.open_start_page()
        login_page.click_register_link()
        register_page.enter_username(payload.valid_created_payload["username"])
        register_page.enter_password(payload.valid_created_payload["password"])
        register_page.click_register()
        if "register" in driver.current_url:
            register_page.click_login_link()
        login_page.click_element(login_page.LOGIN_LINK)
        login_page.enter_username(payload.valid_created_payload["username"])
        login_page.enter_password(payload.valid_created_payload["password"])
        login_page.click_login()
        save_screenshot(driver, folder_path="screenshots/UI/e2e", filename_prefix="user_logged_in")

    with allure.step("Нажимем на кнопку создания новой задачи:"):
        tasks_page = TasksPage(driver)
        tasks_page.click_element(tasks_page.CREATE_TASK_BUTTON)
        save_screenshot(driver, folder_path="screenshots/UI/e2e", filename_prefix="task_page")

    with allure.step("Заполняем название и описание для таски"):
        create_task = CreateTaskPage(driver)
        create_task.create_new_task("task", "some description")
        save_screenshot(driver, folder_path="screenshots/UI/e2e",\
                        filename_prefix="task_has_been_created_alarm")
        assert "Задача успешно создана" in tasks_page.get_alert_message(tasks_page.SUCCESS_ALERT)

    with allure.step("Переходим на страницу просмотра таски и отмечаем её как выполненую"):
        taskid = 1
        tasks_page.view_task(taskid=taskid)
        view_task = ViewTask(driver)
        view_task.click_element(view_task.TOGGLE_STATUS_BUTTON)
        save_screenshot(driver, folder_path="screenshots/UI/e2e",\
                        filename_prefix="task_toggled_as_completed")
        assert "Задача отмечена как выполнена" in\
               tasks_page.get_alert_message(tasks_page.SUCCESS_ALERT)

    with allure.step("убираем выделение с задачи через страницу с тасками"):
        tasks_page.change_task_status(taskid)
        save_screenshot(driver, folder_path="screenshots/UI/e2e",\
                        filename_prefix="task_toggled_as_incompleted")
        assert "Задача отмечена как не выполнена" in\
               tasks_page.get_alert_message(tasks_page.SUCCESS_ALERT)


    with allure.step("Переименовываем задачу"):
        tasks_page.edit_task(taskid)
        change_task = ChangeTaskPage(driver)
        updated_name = "updated name"
        change_task.update_task(name=updated_name, description="not an empty one this time")
        save_screenshot(driver, folder_path="screenshots/UI/e2e",
                        filename_prefix="task_edited")
        assert "Задача успешно обновлена" in\
               tasks_page.get_alert_message(tasks_page.SUCCESS_ALERT)

    with allure.step("Проверяем, что имя обновилось"):
        assert tasks_page.get_task_name(taskid) ==  updated_name

    with allure.step("обновляем статус задачи, через страницу изменения"):
        tasks_page.edit_task(taskid)
        change_task.click_checkbox()
        save_screenshot(driver, folder_path="screenshots/UI/e2e",\
                        filename_prefix="task_toggled_as_completed")
        assert "Задача успешно обновлена" in\
               tasks_page.get_alert_message(tasks_page.SUCCESS_ALERT)
        tasks_page.change_task_status(taskid=taskid)

    with allure.step("удаляем задачу"):
        tasks_page.delete_task(taskid=taskid)
        modal_window = ModalWindow(driver)
        modal_window.submit_delete(taskid=taskid)
        save_screenshot(driver, folder_path="screenshots/UI/e2e",\
                        filename_prefix="task_deleted")
        assert "Задача успешно удалена" in\
               tasks_page.get_alert_message(tasks_page.SUCCESS_ALERT)
