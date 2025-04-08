import requests
import settings

class BaseEndpoint():
    response_json = None
    schema= {}
    url = settings.url

    def check_response_is_200(self):
        assert self.response.status_code == 200, \
        f"{self.response.status_code}"

    def check_response_is_201(self):
        assert self.response.status_code == 201, \
        f"{self.response.status_code}"
