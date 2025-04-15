"""Unit tests for toggle task status API endpoint."""
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.toggle_task_status import ToggleTaskStatus
from tests.api.payload.payload import valid_task_template

import allure

@allure.feature("API Тесты")
@allure.story("Переключение статуса задачи")
def test_toggle_task_status(session, register_login_user):# pylint: disable=unused-argument
    """Тестирует успешное изменения статуса задачи через API."""
    with allure.step("Создаем задачу"):
        task = CreateTask()
        response = task.create_task(task_data=valid_task_template,\
                                    session=session)
        task_id = response["id"]

    with allure.step("Переключаем статус задачи"):
        toggler = ToggleTaskStatus()
        response = toggler.toggle_task_status(session=session,\
                                              task_id=task_id)

    with allure.step("Проверяем успешность переключения статуса"):
        assert toggler.check_response_is_200()
