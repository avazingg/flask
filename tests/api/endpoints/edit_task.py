import requests
from tests.api.endpoints.base_endpoint import BaseEndpoint

class EditTask(BaseEndpoint):
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

    def edit_task(self, task_id, edited_data, session):
        self.response = session.put(f"{self.url}/api/tasks/{task_id}", json=edited_data, headers=self.headers)
        self.response_json = self.response.json()
        return self.response_json