from tests.api.endpoints.base_endpoint import BaseEndpoint
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.edit_task import EditTask
from tests.api.payload.payload import valid_task_template,\
    valid_edited_task_template
from tests.api.conftest import register_login_user

import allure

@allure.feature("API Тесты")
@allure.story("Редактирование задачи")
def test_edit_task(session, register_login_user):
    user_id = register_login_user["user_id"]
    edited_data = valid_edited_task_template
    task = CreateTask()

    with allure.step("Создаем задачу для редактирования"):
        response = task.create_task(task_data=valid_task_template, session=session)
        task_id = response["id"]
        allure.attach(str(response), name="Созданная задача", attachment_type=allure.attachment_type.JSON)

    edit_task = EditTask()

    with allure.step(f"Редактируем задачу с ID = {task_id}"):
        response = edit_task.edit_task(session=session, task_id=task_id, edited_data=edited_data)
        allure.attach(str(response), name="Отредактированная задача", attachment_type=allure.attachment_type.JSON)

    with allure.step("Проверяем, что название задачи изменилось"):
        assert response["title"] == edited_data["title"], f"Expected title: {edited_data['title']} but got: {response['title']}"