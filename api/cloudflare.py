import requests

class Cloudflare:
    def __init__(self, email, token):
        self.email = email
        self.token = token
        self.base_url = 'https://api.cloudflare.com/client/v4/'

    def api_get(self, url):
        call_url = self.base_url + url
        headers = self.get_headers()
        print(headers)
        print(call_url)
        response = requests.get(call_url, headers=headers)
        return self.process_response(response)

    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

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
