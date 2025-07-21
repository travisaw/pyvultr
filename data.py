import os
import json
import base64

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
    directory = './data'
    file_path = os.path.join(directory, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return None

def load_cloud_init(file_name):
    """
    Loads cloud-init configuration from a file.
    Returns the content of the file as a string or None if the file does not exist.
    """
    directory = './data'
    file_path = os.path.join(directory, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            string_data = f.read()
        bytes_data = string_data.encode('utf-8')
        return base64.b64encode(bytes_data).decode('utf-8')
    else:
        return None
