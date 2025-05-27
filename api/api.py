import requests

class Api():
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

    def api_put(self, url, data):
        call_url = self.base_url + url
        headers = self.get_headers()
        response = requests.put(call_url, json=data, headers=headers)
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
