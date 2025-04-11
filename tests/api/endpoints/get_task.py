import requests
from tests.api.endpoints.base_endpoint import BaseEndpoint


class GetTask(BaseEndpoint):
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "created_at": {"type": "string", "format": "date-time"},
            "completed": {"type": "boolean"},
            "user_id": {"type": "integer"}
        },
        "required": ["id", "title", "description", "created_at", "completed", "user_id"]
    }

    def get_task(self, task_id, session):
        self.response = session.get(f'{self.url}/api/tasks/{task_id}', headers=self.headers)
        self.response_json = self.response.json()
        return self.response_json