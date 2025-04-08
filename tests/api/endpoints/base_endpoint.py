import requests

import settings
import settings


class BaseEndpoint():
    response_json = None
    schema= {}
    url = settings.url
