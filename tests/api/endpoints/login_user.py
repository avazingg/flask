import requests
from flask import session

from tests.api.endpoints.base_endpoint import BaseEndpoint


class LoginUser(BaseEndpoint):
    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "user_id": {"type": "integer"},
            "username": {"type": "string"}
        },
        "required": ["message", "user_id", "username"]
    }

    def login_user(self,user_data, session):
        self.response = session.post(f'{self.url}/api/login',
                                      json=user_data, headers=self.headers)
        self.response_json = self.response.json()
        return self.response_json

    def get_user_id(self):
        return self.response_json.get("user_id")

    def get_username(self):
        return self.response_json.get("username")

    def get_password(self):
        return self.response_json.get("password")