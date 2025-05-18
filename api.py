import requests

class Api:
    def __init__(self, token):
        self.token = token
        self.base_url = 'https://api.vultr.com/v2/'

    def api_get(self, url):
        call_url = self.base_url + url
        headers = self.get_headers()    
        response = requests.get(call_url, headers=headers)
        return self.process_response(response)

    def api_post(self, url, data):
        call_url = self.base_url + url
        headers = self.get_headers()    
        response = requests.post(call_url, json=data, headers=headers)
        return self.process_response(response)

    def api_delete(self, url):
        call_url = self.base_url + url
        headers = self.get_headers()    
        response = requests.delete(call_url, headers=headers)
        return self.process_response(response)
    
    def get_headers(self):
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json' # Adjust content type if needed
        }
    
    def process_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: {response.status_code}, {response.text}"