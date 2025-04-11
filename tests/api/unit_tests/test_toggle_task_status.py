from tests.api.endpoints.base_endpoint import BaseEndpoint
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.edit_task import EditTask
from tests.api.endpoints.toggle_task_status import ToggleTaskStatus
from tests.api.payload.payload import valid_task_template,\
    valid_edited_task_template
from tests.api.conftest import register_login_user

import allure

@allure.feature("API Тесты")
@allure.story("Переключение статуса задачи")
def test_toggle_task_status(session, register_login_user):
    with allure.step("Создаем задачу"):
        task = CreateTask()
        response = task.create_task(task_data=valid_task_template, session=session)
        task_id = response["id"]

    with allure.step("Переключаем статус задачи"):
        toggler = ToggleTaskStatus()
        response = toggler.toggle_task_status(session=session, task_id=task_id)

    with allure.step("Проверяем успешность переключения статуса"):
        assert toggler.check_response_is_200()