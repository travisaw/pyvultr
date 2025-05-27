import requests
from .api import Api

class Vultr(Api):
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.vultr.com/v2/'

    def process_response(self, response):
        try:
            output = response.json()
            # print(output)
        except requests.exceptions.JSONDecodeError:
            output = {'info': 'No response body.', 'status': response.status_code}

        if response.status_code >= 200 and response.status_code < 300:
            return output
        else:
            return {'error': response.status_code, 'error_detail': output}
