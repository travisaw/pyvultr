import requests

def call_api_with_token(url, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json' # Adjust content type if needed
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: {response.status_code}, {response.text}"
