from app import tasks
from tests.api.endpoints.base_endpoint import BaseEndpoint
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.create_task import CreateTask
from tests.api.payload.payload import valid_task_template,\
    invalid_task_template_no_title, invalid_task_template_no_description
from tests.api.conftest import register_login_user

import allure


@allure.feature("API Тесты")
@allure.story("Создание задачи — валидный сценарий")
def test_create_task(session, register_login_user):
    user_id = register_login_user["user_id"]
    task_data = valid_task_template
    task = CreateTask()

    with allure.step("Создаем новую задачу с валидными данными"):
        response = task.create_task(task_data=task_data, session=session)

    with allure.step("Проверяем, что название задачи совпадает с отправленным"):
        assert response["title"] == task_data["title"], f"Expected title: {task_data['title']} but got: {response['title']}"

    with allure.step("Проверяем, что задача принадлежит правильному пользователю"):
        assert response["user_id"] == user_id, f"Expected user_id: {user_id} but got: {response['user_id']}"


@allure.feature("API Тесты")
@allure.story("Создание задачи — без заголовка")
def test_create_task_without_title(session, register_login_user):
    task_data = invalid_task_template_no_title
    task = CreateTask()

    with allure.step("Пытаемся создать задачу без заголовка"):
        response = task.create_task(task_data=task_data, session=session)

    with allure.step("Проверяем, что API возвращает 400 Bad Request"):
        task.check_response_is_400(), "response must be 400, not 201 — нельзя создать задачу без заголовка"

    with allure.step("Логируем ответ"):
        allure.attach(str(response), name="Ответ API", attachment_type=allure.attachment_type.JSON)


@allure.feature("API Тесты")
@allure.story("Создание задачи — без описания")
def test_create_task_without_description(session, register_login_user):
    task_data = invalid_task_template_no_description
    task = CreateTask()

    with allure.step("Создаем задачу только с заголовком, без описания"):
        response = task.create_task(task_data=task_data, session=session)

    with allure.step("Проверяем, что API возвращает 201 Created"):
        task.check_response_is_201(), "response must be 201 — допускается создание задачи только с заголовком"

    with allure.step("Логируем ответ"):
        allure.attach(str(response), name="Ответ API", attachment_type=allure.attachment_type.JSON)
