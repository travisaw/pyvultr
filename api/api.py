import requests
import settings
from util import green_text, yellow_text, red_text, blue_text

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

    green_codes = [200, 204]
    yellow_codes = [404]
    red_codes = [500]

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
        self.__print_response_summary(response)
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
        self.__print_response_summary(response)
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
        self.__print_response_summary(response)
        return self.process_response(response)

    def api_patch(self, url, data):
        """
        Sends a PATCH request to the specified API endpoint with the provided data.

        Args:
            url (str): The API endpoint (relative to the base URL) to send the PATCH request to.
            data (dict): The JSON-serializable data to include in the PATCH request body.

        Returns:
            Any: The processed response from the API, as returned by `self.process_response`.

        Raises:
            requests.RequestException: If the PATCH request fails due to a network problem.
            Exception: If `self.process_response` raises an exception.
        """
        call_url = self.base_url + url
        headers = self.__get_headers()
        response = requests.patch(call_url, json=data, headers=headers)
        self.__print_response_summary(response)
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
        self.__print_response_summary(response)
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

    def __print_response_summary(self, response):
        """
        Prints a summary of the HTTP response, including status code and headers.

        Args:
            response (requests.Response): The HTTP response object to summarize.
        """
        if settings.PRINT_API_RESPONSE_SUMMARY:
            url = response.url
            url_display = url[:50] + "..." if len(url) > 30 else url
            print(blue_text(f"URL: {url_display}"))
            print(self.__get_response_code_color(response.status_code))
            print(self.__get_response_time_color(response.elapsed.total_seconds()))
            # print("Response Headers:")
            # for key, value in response.headers.items():
            #     print(f"{key}: {value}")

    def __get_response_time_color(self, seconds):
        """
        Returns a color-formatted string representing the API response time.

        Args:
            seconds (float): The response time in seconds.

        Returns:
            str: The response time string colored green (< 3s), yellow (3–8s), or red (> 8s).
        """
        response_text = f"Response Time: {seconds} seconds"
        if seconds < 3:
            return green_text(response_text)
        if seconds <= 8:
            return yellow_text(response_text)
        return red_text(response_text)

    def __get_response_code_color(self, response_code):
        """
        Returns a color-formatted string representing the HTTP response status code.

        Args:
            response_code (int): The HTTP status code from the response.

        Returns:
            str: The status code string colored green (2xx success), yellow (404), or red (500).
                 Returns the raw status code if it does not match any defined category.
        """
        response_text = f"Response Status Code: {response_code}"
        if response_code in self.green_codes:
            return green_text(response_text)
        if response_code in self.yellow_codes:
            return yellow_text(response_text)
        if response_code in self.red_codes:
            return red_text(response_text)
        else:
            return response_code
