import requests
from tests.api.endpoints.base_endpoint import BaseEndpoint

class CreateTask(BaseEndpoint):
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "completed": {"type": "boolean"},
            "user_id": {"type": "integer"}
        },
        "required": ["title", "description", "created_at", "completed", "user_id"]
    }

    def create_task(self, task_data, session):
        self.response = session.post(f'{self.url}/api/tasks', json=task_data, headers=self.headers)
        self.response_json = self.response.json()
        return self.response_json