import requests
from .api import Api

class Vultr(Api):
    """
    A client for interacting with the Vultr API.
    Args:
        token (str): The API token used for authenticating requests.
    Attributes:
        token (str): The API token.
        base_url (str): The base URL for the Vultr API.
    Methods:
        process_response(response):
            Processes the HTTP response from the Vultr API.
            Attempts to parse the response as JSON. If parsing fails, returns a dictionary with status code and info.
            Returns the parsed output for successful responses (status code 2xx).
            Returns a dictionary with error details for unsuccessful responses.
    """

    def __init__(self, token):
        """
        Initialize the API client with the provided authentication token.

        Args:
            token (str): The API token used for authenticating requests.

        Attributes:
            token (str): Stores the provided API token.
            base_url (str): The base URL for the Vultr API v2.
        """
        self.token = token
        self.base_url = 'https://api.vultr.com/v2/'

    def process_response(self, response):
        """
        Processes the API response specific to the Vultr API.
        Attempts to parse the response body as JSON. If parsing fails, returns a dictionary
        with an informational message and the HTTP status code. For successful responses
        (status code 2xx), returns the parsed JSON output. For unsuccessful responses,
        returns a dictionary containing the error status code and the parsed output or error details.
        Args:
            response (requests.Response): The HTTP response object returned by the requests library.
        Returns:
            dict: The parsed JSON response for successful requests, or a dictionary with error details for failed requests.
        """
        try:
            output = response.json()
            # print(output)
        except requests.exceptions.JSONDecodeError:
            output = {'info': 'No response body.', 'status': response.status_code}

        if response.status_code >= 200 and response.status_code < 300:
            return output
        else:
            return {'error': response.status_code, 'error_detail': output}
