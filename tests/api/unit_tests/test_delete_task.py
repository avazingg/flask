"""Unit tests for the task deletion API endpoint."""
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.delete_task import DeleteTask
from tests.api.payload.payload import valid_task_template

import allure
import pytest


@allure.feature("API Тесты")
@allure.story("Удаление задачи")
def test_delete(session, register_login_user): # pylint: disable=unused-argument
    """Тестирует успешное удаление задачи через API."""
    task_data = valid_task_template
    task = CreateTask()

    with allure.step("Создаем задачу для последующего удаления"):
        response = task.create_task(task_data=task_data, session=session)
        task_id = response["id"]
        allure.attach(str(response), name="Созданная задача",\
                      attachment_type=allure.attachment_type.JSON)

    delete_task = DeleteTask()

    with allure.step(f"Удаляем задачу с ID = {task_id}"):
        delete_task.delete_task(session=session, task_id=task_id)

    with allure.step("Проверяем, что задача успешно удалена (204 No Content)"):
        delete_task.check_response_is_204()
