"""Unit tests for get the task by ID API endpoint."""
from tests.api.endpoints.get_task import GetTask
from tests.api.endpoints.create_task import CreateTask
from tests.api.payload.payload import valid_task_template

import allure

@allure.feature("API Тесты")
@allure.story("Получение задачи")
def test_get_task(session, register_login_user):# pylint: disable=unused-argument
    """Тестирует успешное получение задачи через API."""
    task_data = valid_task_template
    task = CreateTask()
    get_task = GetTask()

    with allure.step("Создаем задачу"):
        task.create_task(task_data=task_data, session=session)

    with allure.step("Получаем задачу по ID = 1"):
        response = get_task.get_task(task_id=1, session=session)
        get_task.check_response_is_200()
        allure.attach(str(response), name="Полученная задача",\
                      attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем, что полученные данные корректны"):
        assert response["title"] == task_data["title"],\
            f"Expected title: {task_data['title']}, but got: {response['title']}"
