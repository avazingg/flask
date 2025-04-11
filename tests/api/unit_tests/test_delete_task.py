from tests.api.endpoints.base_endpoint import BaseEndpoint
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.edit_task import EditTask
from tests.api.endpoints.delete_task import DeleteTask
from tests.api.payload.payload import valid_task_template,\
    valid_edited_task_template
from tests.api.conftest import register_login_user

import allure


@allure.feature("API Тесты")
@allure.story("Удаление задачи")
def test_delete(session, register_login_user):
    user_id = register_login_user["user_id"]
    task_data = valid_task_template
    task = CreateTask()

    with allure.step("Создаем задачу для последующего удаления"):
        response = task.create_task(task_data=task_data, session=session)
        task_id = response["id"]
        allure.attach(str(response), name="Созданная задача", attachment_type=allure.attachment_type.JSON)

    delete_task = DeleteTask()

    with allure.step(f"Удаляем задачу с ID = {task_id}"):
        response = delete_task.delete_task(session=session, task_id=task_id)

    with allure.step("Проверяем, что задача успешно удалена (204 No Content)"):
        delete_task.check_response_is_204(), "response must be: 204"