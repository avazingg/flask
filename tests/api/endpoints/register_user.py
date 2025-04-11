import requests
from tests.api.endpoints.base_endpoint import BaseEndpoint


class RegisterUser(BaseEndpoint):

    schema = {
        "type": "object",
        "properties": {
            "message": {"type": "string"}
        },
        "required": ["message"]
    }
    def register_user(self, user_data, session):
        self.response = session.post(f'{self.url}/api/register',
                                      json=user_data, headers=self.headers)
        self.response_json = self.response.json()
        return self.response_json