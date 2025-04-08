from app import db

import allure
import pytest


# @pytest.fixture(scope="session"):
# def cleanup_db(db_connection):
#     yield
#     cursor = db_connection.cursor()
#     cursor.e