import os
import json
import base64
import requests

def create_data_cache(file_name, data):
    """
    Creates a directory and a file for data caching if they do not exist.
    The directory is './data' and the file is 'plans.json'.
    """
    # Define the directory and file path
    directory = './data'
    file_path = os.path.join(directory, file_name)

    formatted_json = json.dumps(data, indent=2)

    # Create directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create file if it doesn't exist
    # if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        f.write(formatted_json)  # You can write default content here

def load_data_cache(file_name):
    """
    Loads data from the cache file if it exists.
    Returns the data as a dictionary or None if the file does not exist.
    """
    directory = 'data'
    file_path = os.path.join('.', directory, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return None

def load_cloud_init_http(url):
    """
    Fetches cloud-init configuration from a given HTTP URL, encodes it in base64, and returns the encoded string.
    Args:
        url (str): The HTTP URL to fetch the cloud-init configuration from.
    Returns:
        str or None: The base64-encoded cloud-init configuration as a string if successful, otherwise None.
    Raises:
        None: All exceptions are caught and handled internally.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx, 5xx)

        string_data = response.text
        bytes_data = string_data.encode('utf-8')
        return base64.b64encode(bytes_data).decode('utf-8')

    except requests.exceptions.RequestException as e:
        print(f"Error fetching cloud-init from {url}: {e}")
        return None

def load_cloud_init_local(file_name):
    """
    Loads cloud-init configuration from a file.
    Returns the content of the file as a string or None if the file does not exist.
    """
    directory = 'data'
    file_path = os.path.join('.', directory, file_name)

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            string_data = f.read()
        bytes_data = string_data.encode('utf-8')
        return base64.b64encode(bytes_data).decode('utf-8')
    else:
        print(f"{file_name} doesn't exist!")
        return None
