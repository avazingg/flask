from app import db, User, Task
from app import app
from sqlalchemy import text

def restart_whole_db():
    with app.app_context():
        Task.query.delete()
        User.query.delete()
        db.session.execute(text('ALTER SEQUENCE user_id_seq RESTART WITH 1;'))
        db.session.execute(text('ALTER SEQUENCE task_id_seq RESTART WITH 1;'))
        db.session.commit()

def show_db():
    with app.app_context():
        tasks = Task.query.all()
        users = User.query.all()
        for task in tasks:
            print(f'ID: {task.id}, Title: {task.title}, Description: {task.description}')
        for user in users:
            print(f'ID: {user.id}, Username: {user.username}')

if __name__ == "__main__":
    restart_whole_db()
    show_db()