import requests
from tests.api.endpoints.base_endpoint import BaseEndpoint

class DeleteTask(BaseEndpoint):
    def delete_task(self, task_id, session):
        self.response = session.delete(f'{self.url}/api/tasks/{task_id}',  headers=self.headers)
        return self.response