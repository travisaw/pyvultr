from util import utc_to_local
from tabulate import tabulate

def get_account_info(api):
    """Print account info."""
    url = 'account'
    data = api.api_get(url)
    result = [
        ['Name: ', data['account']['name']],
        ['Email: ', data['account']['email']],
        ['Balance: ', data['account']['balance']],
        ['Pending Charges: ', data['account']['pending_charges']],
        ['Last Payment Date: ', utc_to_local(data['account']['last_payment_date'])],
        ['Last Payment Amount: ', data['account']['last_payment_amount']]
    ]
    print(tabulate(result))
