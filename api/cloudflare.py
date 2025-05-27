import requests
from .api import Api

class Cloudflare(Api):
    def __init__(self, email, token):
        self.email = email
        self.token = token
        self.base_url = 'https://api.cloudflare.com/client/v4/'

    def process_response(self, response):
        """Processes API response which is specific to the Cloudflare API."""
        try:
            output = response.json()
            # print(output)
        except requests.exceptions.JSONDecodeError:
            output = {'info': 'No response body.', 'status': response.status_code}

        if response.status_code >= 200 and response.status_code < 300:
            return output
        else:
            return {'error': response.status_code, 'error_detail': output}
