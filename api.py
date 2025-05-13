import requests

class Api:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.vultr.com/v2/'

    def call_api_with_token(self, url):
        call_url = self.base_url + url
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json' # Adjust content type if needed
        }
    
        response = requests.get(call_url, headers=headers)
    
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.text}"
