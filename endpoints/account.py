from util import utc_to_local

def get_account_info(api):
    url = 'account'
    data = api.call_api_with_token(url)
    print('Name: ', data['account']['name'])
    print('Email: ', data['account']['email'])
    print('Balance: ', data['account']['balance'])
    print('Pending Charges: ', data['account']['pending_charges'])
    print('Last Payment Date: ', utc_to_local(data['account']['last_payment_date']))
    print('Last Payment Amount: ', data['account']['last_payment_amount'])
