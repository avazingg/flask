# from app import db, User, Task
# from app import app
# from sqlalchemy import text
#
# def restart_whole_db():
#     with app.app_context():
#         Task.query.delete()
#         User.query.delete()
#         db.session.execute(text('ALTER SEQUENCE user_id_seq RESTART WITH 1;'))
#         db.session.execute(text('ALTER SEQUENCE task_id_seq RESTART WITH 1;'))
#         db.session.commit()
#
# def show_db():
#     with app.app_context():
#         tasks = Task.query.all()
#         users = User.query.all()
#         for task in tasks:
#             print(f'ID: {task.id}, Title: {task.title}, Description: {task.description}')
#         for user in users:
#             print(f'ID: {user.id}, Username: {user.username}')
#
#
# def add_user_to_db(username, password):
#     with app.app_context():
#         # Создаем нового пользователя
#         new_user = User(username=username, password=password)
#
#         # Добавляем пользователя в базу данных
#         db.session.add(new_user)
#
#         # Сохраняем изменения в базе данных
#         db.session.commit()
#
# if __name__ == "__main__":
#     restart_whole_db()
#     show_db()
from app import db, User, Task
from app import app
from sqlalchemy import text


class DatabaseManager:
    def __init__(self):
        self.app = app

    def restart_whole_db(self):
        """Перезапускает базу данных (удаляет все записи и сбрасывает последовательности)"""
        with self.app.app_context():
            Task.query.delete()
            User.query.delete()
            db.session.execute(text('ALTER SEQUENCE user_id_seq RESTART WITH 1;'))
            db.session.execute(text('ALTER SEQUENCE task_id_seq RESTART WITH 1;'))
            db.session.commit()

    def show_db(self):
        """Выводит все задачи и пользователей в базе данных"""
        with self.app.app_context():
            tasks = Task.query.all()
            users = User.query.all()
            for task in tasks:
                print(f'ID: {task.id}, Title: {task.title}, Description: {task.description}')
            for user in users:
                print(f'ID: {user.id}, Username: {user.username}')

    def add_user_to_db(self, username, password):
        """Добавляет нового пользователя в базу данных"""
        with self.app.app_context():
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()


if __name__ == "__main__":
    # Пример использования класса
    db_manager = DatabaseManager()

    # # Перезапускаем БД
    # db_manager.restart_whole_db()

    # Показываем состояние базы данных
    db_manager.show_db()
