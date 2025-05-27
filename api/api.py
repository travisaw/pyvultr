import requests

class Api():
    """Parent API calss containing methods common to all API subclasses."""
    def api_get(self, url):
        """HTTP GET. Provide URL and results are returned."""
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.get(call_url, headers=headers)
        return self.process_response(response)

    def api_post(self, url, data):
        """HTTP POST. Provide URL and body and results are returned."""
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.post(call_url, json=data, headers=headers)
        return self.process_response(response)

    def api_put(self, url, data):
        """HTTP PUT. Provide URL and body and results are returned."""
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.put(call_url, json=data, headers=headers)
        return self.process_response(response)

    def api_delete(self, url):
        """HTTP DELETE. Provide URL and results are returned."""
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.delete(call_url, headers=headers)
        return self.process_response(response)

    def __get_headers(self):
        """Private function to return common http request headers across all API calls."""
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json' # Adjust content type if needed
        }
