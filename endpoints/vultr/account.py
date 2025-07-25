from util import utc_str_to_local, print_output_table, format_currency

def get_account_info(api):
    """
    Retrieves and prints the account information using the provided API client.

    Args:
        api: An API client instance with an `api_get` method for fetching account data.

    Returns:
        None. Prints a formatted table of account information to the console.

    Raises:
        KeyError: If expected keys are missing in the API response.
        Exception: Propagates exceptions raised by the API client or utility functions.
    """
    url = 'account'
    data = api.api_get(url)
    result = [
        ['Name: ', data['account']['name']],
        ['Email: ', data['account']['email']],
        ['Balance: ', format_currency(data['account']['balance'])],
        ['Pending Charges: ', format_currency(data['account']['pending_charges'])],
        ['Last Payment Date: ', utc_str_to_local(data['account']['last_payment_date'])],
        ['Last Payment Amount: ', format_currency(data['account']['last_payment_amount'])]
    ]
    print_output_table(result)
