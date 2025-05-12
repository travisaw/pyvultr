from api import call_api_with_token

def account(url, api_key):
  url += 'account'
  print(call_api_with_token(url, api_key))
  return 'Account'
