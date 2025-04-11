import requests
import settings

class BaseEndpoint():
    response = None
    response_json = None
    schema= {}
    url = settings.url
    headers = {"Content-Type": "application/json"}

    def check_response_is_200(self):
        assert self.response.status_code == 200, \
        f"{self.response.status_code}"
        return True

    def check_response_is_201(self):
        assert self.response.status_code == 201, \
        f"{self.response.status_code}"
        return True

    def check_response_is_204(self):
        assert self.response.status_code == 204, \
        f"{self.response.status_code}"

    def check_response_is_400(self):
        assert self.response.status_code == 400, \
            f"{self.response.status_code}"

    def check_response_is_401(self):
        assert self.response.status_code == 401, \
        f"{self.response.status_code}"

    def get_data(self):
        return self.response.json()

    def get_messgae(self):
        return self.response.json()["message"]

    def get_error(self):
        return self.response.json()["error"]

    def get_task_title(self):
        return self.response.json()["title"]

    def get_task_description(self):
        return self.response.json()["description"]

    def ger_task_status(self):
        return self.response.json()["completed"]

    def check_all_fields(self, expected_data):
        assert self.get_data()["data"] == expected_data["data"], "wrong data in it"
