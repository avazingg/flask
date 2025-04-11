import allure
from tests.api.endpoints.create_task import CreateTask
from tests.api.endpoints.edit_task import EditTask
from tests.api.endpoints.get_task import GetTask
from tests.api.endpoints.login_user import LoginUser
from tests.api.endpoints.register_user import RegisterUser
from tests.api.endpoints.toggle_task_status import ToggleTaskStatus
from tests.api.endpoints.delete_task import DeleteTask
from tests.api.payload.payload import valid_task_template, valid_edited_task_template
from tests.api.conftest import register_login_user
from db_interaction import DatabaseManager


@allure.feature("API Тест")
@allure.story("Полный цикл работы с задачами через API")
def test_e2e_task_management_api(session):
    # Шаг 1: Обнуление БД перед началом теста
    db = DatabaseManager()
    db.restart_whole_db()
    test_user = {
        "username": "apiuser1",
        "password": "apiuser"
    }
    # Шаг 2: Регистрируем нового пользователя
    with allure.step("Регистрируем нового пользователя"):
        register = RegisterUser()
        response_json = register.register_user(test_user, session)

    with allure.step("Проверяем успешную регистрацию"):
        register.check_response_is_201()
        assert "Регистрация успешна" in response_json["message"], \
            "получено другое сообщение"

    # Шаг 3: Логинимся созданным Юзером
    with allure.step("Логинимся созданным Юзером"):
        login_user = LoginUser()
        response_json = login_user.login_user(test_user, session)
        user_id = response_json["user_id"]

    with allure.step("Проверяем успешный вход в систему"):
        assert response_json["message"] == "Вы успешно вошли в систему", \
            f"Expected message 'Вы успешно вошли в систему' but got {response_json['message']}"
        assert user_id == response_json["user_id"], \
            f"Expected user_id {user_id} but got {response_json['user_id']}"
        assert response_json["username"] == test_user["username"], \
            f"Expected username {test_user['username']} but got {response_json['username']}"

    # Шаг 4: Создаем новую задачу
    with allure.step("Создаем новую задачу через API"):
        task_data = valid_task_template
        task = CreateTask()
        response = task.create_task(task_data=valid_task_template, session=session)
        task_id = response["id"]  # Получаем ID задачи после создания

        assert response["title"] == valid_task_template[
            "title"], f"Expected title: {valid_task_template['title']} but got: {response['title']}"
        assert response["description"] == valid_task_template[
            "description"], f"Expected description: {valid_task_template['description']} but got: {response['description']}"

    # Шаг 5: Получаем задачу по id
    with allure.step("Получаем задачу по id"):
        get_task = GetTask()
        response = get_task.get_task(task_id=1, session=session)

    with allure.step("Проверяем, что полученные данные корректны"):
        assert response["title"] == task_data[
            "title"], f"Expected title: {task_data['title']}, but got: {response['title']}"

    # Шаг 6: Переключение статуса задачи
    with allure.step("Переключаем статус задачи через API"):
        toggler = ToggleTaskStatus()
        response = toggler.toggle_task_status(session=session, task_id=task_id)
        assert toggler.check_response_is_200(), "Expected status code 200, but got {response.status_code}"

    # Шаг 7: Обновление задачи
    with allure.step("Обновляем информацию о задаче через API"):
        edit_task = EditTask()
        response = edit_task.edit_task(session=session, task_id=task_id, edited_data=valid_edited_task_template)
        assert response["title"] == valid_edited_task_template[
            "title"], f"Expected updated title: {valid_edited_task_template['title']} but got: {response['title']}"
        assert response["description"] == valid_edited_task_template[
            "description"], f"Expected updated description: {valid_edited_task_template['description']} but got: {response['description']}"

    # Шаг 8: Удаление задачи
    with allure.step("Удаляем задачу через API"):
        delete_task = DeleteTask()
        response = delete_task.delete_task(session=session, task_id=task_id)
        delete_task.check_response_is_204(), f"Expected status code 204, but got {response.status_code}"
