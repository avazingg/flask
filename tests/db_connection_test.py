import pytest
import psycopg2
import os
import time

def test_database_connection():
    """Тест подключения к базе данных PostgreSQL"""
    # Параметры подключения из переменных окружения или значения по умолчанию
    db_params = {
        'dbname': os.environ.get('POSTGRES_DB', 'taskmanager'),
        'user': os.environ.get('POSTGRES_USER', 'postgres'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'host': os.environ.get('POSTGRES_HOST', 'db'),
        'port': os.environ.get('POSTGRES_PORT', '5432')
    }
    
    # Максимальное количество попыток подключения
    max_retries = 5
    retry_interval = 2
    
    # Попытки подключения с повторами
    for attempt in range(max_retries):
        try:
            print(f"\nПопытка подключения к базе данных {attempt+1}/{max_retries}")
            print(f"Параметры подключения: {db_params}")
            
            # Установка соединения
            conn = psycopg2.connect(**db_params)
            
            # Создание курсора
            cursor = conn.cursor()
            
            # Проверка соединения простым запросом
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"Версия PostgreSQL: {version[0]}")
            
            # Проверка наличия таблиц
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """)
            tables = cursor.fetchall()
            print("Таблицы в базе данных:")
            for table in tables:
                print(f"- {table[0]}")
            
            # Если есть таблица task, проверим её структуру
            if any(table[0] == 'task' for table in tables):
                cursor.execute("""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'task'
                """)
                columns = cursor.fetchall()
                print("\nСтруктура таблицы task:")
                for column in columns:
                    print(f"- {column[0]}: {column[1]}")
                
                # Проверка количества записей
                cursor.execute("SELECT COUNT(*) FROM task")
                count = cursor.fetchone()[0]
                print(f"\nКоличество записей в таблице task: {count}")
                
                # Если есть записи, выведем первые 5
                if count > 0:
                    cursor.execute("""
                        SELECT id, title, description, completed, user_id 
                        FROM task 
                        LIMIT 5
                    """)
                    tasks = cursor.fetchall()
                    print("\nПримеры задач:")
                    for task in tasks:
                        print(f"ID: {task[0]}, Название: {task[1]}, Выполнено: {task[3]}, ID пользователя: {task[4]}")
            
            # Закрытие курсора и соединения
            cursor.close()
            conn.close()
            
            print("\nПодключение к базе данных успешно!")
            return  # Успешное подключение, выходим из функции
            
        except psycopg2.OperationalError as e:
            print(f"Ошибка подключения: {e}")
            if attempt < max_retries - 1:
                print(f"Повторная попытка через {retry_interval} секунд...")
                time.sleep(retry_interval)
            else:
                print("Превышено максимальное количество попыток подключения.")
                raise  # Пробрасываем исключение после всех попыток
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
            raise

if __name__ == "__main__":
    test_database_connection()
