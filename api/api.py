import requests

class Api():
    """
    Parent API class containing methods common to all API subclasses.
    Methods
    -------
    api_get(url)
        Sends an HTTP GET request to the specified URL and returns the processed response.
    api_post(url, data)
        Sends an HTTP POST request with the provided data to the specified URL and returns the processed response.
    api_put(url, data)
        Sends an HTTP PUT request with the provided data to the specified URL and returns the processed response.
    api_delete(url)
        Sends an HTTP DELETE request to the specified URL and returns the processed response.
    __get_headers()
        Private method that returns the common HTTP request headers used in all API calls.
    """

    def api_get(self, url):
        """
        Sends an HTTP GET request to the specified API endpoint.

        Args:
            url (str): The endpoint path to append to the base URL for the GET request.

        Returns:
            Any: The processed response from the API, as returned by `process_response`.

        Raises:
            requests.RequestException: If the HTTP request fails.
            Exception: If response processing fails.
        """
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.get(call_url, headers=headers)
        return self.process_response(response)

    def api_post(self, url, data):
        """
        Sends an HTTP POST request to the specified API endpoint.

        Args:
            url (str): The API endpoint (relative to the base URL) to send the POST request to.
            data (dict): The JSON-serializable data to include in the body of the POST request.

        Returns:
            Any: The processed response from the API, as returned by `process_response`.

        Raises:
            requests.RequestException: If the HTTP request fails.
            Exception: If the response processing fails.
        """
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.post(call_url, json=data, headers=headers)
        return self.process_response(response)

    def api_put(self, url, data):
        """
        Sends an HTTP PUT request to the specified URL with the provided data.

        Args:
            url (str): The endpoint URL (relative to the base URL) to send the PUT request to.
            data (dict): The JSON-serializable data to include in the request body.

        Returns:
            Any: The processed response from the server, as returned by `process_response`.

        Raises:
            requests.RequestException: If the HTTP request fails.
        """
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.put(call_url, json=data, headers=headers)
        return self.process_response(response)

    def api_delete(self, url):
        """
        Sends an HTTP DELETE request to the specified URL.

        Args:
            url (str): The endpoint path to append to the base URL for the DELETE request.

        Returns:
            Any: The processed response from the DELETE request.

        Raises:
            requests.RequestException: If the HTTP request fails.
            Exception: If response processing fails.
        """
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.delete(call_url, headers=headers)
        return self.process_response(response)

    def __get_headers(self):
        """
        Returns a dictionary of common HTTP request headers used for API calls.

        The headers include:
        - 'Authorization': Bearer token for authentication.
        - 'Content-Type': Specifies the media type of the request body (default is 'application/json').

        Returns:
            dict: A dictionary containing HTTP headers for API requests.
        """
        return {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json' # Adjust content type if needed
        }
