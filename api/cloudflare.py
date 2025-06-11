import requests
from .api import Api

class Cloudflare(Api):
    """
    Cloudflare API client for interacting with the Cloudflare v4 API.
    Args:
        email (str): The email address associated with the Cloudflare account.
        token (str): The API token for authenticating requests.
    Attributes:
        email (str): The email address used for authentication.
        token (str): The API token used for authentication.
        base_url (str): The base URL for the Cloudflare v4 API.
    Methods:
        process_response(response):
            Processes the HTTP response from the Cloudflare API.
            Attempts to parse the response as JSON. If parsing fails, returns a dictionary with status code and info.
            Returns the parsed output for successful responses (status code 2xx).
            Returns a dictionary with error details for unsuccessful responses.
    """

    def __init__(self, email, token):
        """
        Initializes the Cloudflare API client with the provided email and API token.

        Args:
            email (str): The email address associated with the Cloudflare account.
            token (str): The API token for authenticating requests to the Cloudflare API.
        """
        self.email = email
        self.token = token
        self.base_url = 'https://api.cloudflare.com/client/v4/'

    def process_response(self, response):
        """
        Processes the API response specific to the Cloudflare API.
        Attempts to parse the response body as JSON. If parsing fails, returns a dictionary
        with an informational message and the HTTP status code. For successful responses
        (status code 2xx), returns the parsed JSON output. For unsuccessful responses,
        returns a dictionary containing the error status code and the parsed output or error details.
        Args:
            response (requests.Response): The HTTP response object returned by the API request.
        Returns:
            dict: The parsed JSON output for successful responses, or a dictionary with error
            information for unsuccessful responses.
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
