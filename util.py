from datetime import datetime, timezone as tz
import pytz
import tzlocal
import ipaddress
from tabulate import tabulate
import settings

def utc_str_to_local(utc_string):
    """
    Converts a UTC datetime string to a local datetime object.

    Args:
        utc_string (str): A string representing a UTC datetime.

    Returns:
        datetime: The corresponding local datetime object.

    Raises:
        ValueError: If the input string cannot be parsed as a valid UTC datetime.
    """
    utc_dt = get_utc_dt(utc_string)
    return utc_to_local(utc_dt)

def utc_to_local(utc_dt):
    """
    Converts a UTC datetime object to a string representing the local time zone.
    Args:
        utc_dt (datetime.datetime): A timezone-aware datetime object in UTC.
    Returns:
        str: The localized datetime as a string in the format "YYYY-MM-DD HH:MM:SS TZ".
    Raises:
        AttributeError: If `utc_dt` is not timezone-aware.
    Example:
        >>> import pytz, tzlocal, datetime
        >>> utc_dt = datetime.datetime(2024, 6, 1, 12, 0, 0, tzinfo=pytz.UTC)
        >>> utc_to_local(utc_dt)
        '2024-06-01 08:00:00 EDT'
    """
    # Get timezone of local system
    timezone = str(tzlocal.get_localzone()) # IE: America/New_York

    # Localize the UTC datetime object
    local_tz = pytz.timezone(timezone)  # Replace with your desired local timezone
    local_dt = utc_dt.astimezone(local_tz)

    # Convert back to a string in a specific format
    local_dt_string = local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    return local_dt_string

def hour_minutee_day_diff(utc_string):
    """
    Calculates the difference between the current UTC time and a given UTC datetime string,
    returning a human-readable string representing the number of days, hours, and minutes.
    Args:
        utc_string (str): A string representing a UTC datetime.
    Returns:
        str: A string describing the time difference in days, hours, and minutes,
             or "Less than a minute" if the difference is less than one minute.
    """
    utc_now = get_utc_now()
    utc_dt = get_utc_dt(utc_string)

    delta = utc_now - utc_dt
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    parts = []
    if days >= 1:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours >= 1:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes >= 1:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    return ", ".join(parts) if parts else "Less than a minute"

def get_utc_dt(utc_string):
    """
    Converts a UTC datetime string to a timezone-aware datetime object.
    Args:
        utc_string (str): The UTC datetime string to convert.
    Returns:
        datetime: A timezone-aware datetime object in UTC.
    Raises:
        ValueError: If the utc_string does not match the detected format.
    Note:
        The function relies on `detect_datetime_format` to determine the format of the input string.
    """
    utc_format = detect_datetime_format(utc_string)

    # Parse the UTC string into a datetime object
    utc_dt = datetime.strptime(utc_string, utc_format)
    utc_dt = utc_dt.replace(tzinfo=tz.utc)
    return utc_dt

def get_utc_now():
    """
    Returns the current UTC datetime.

    Uses the pytz library to ensure the returned datetime is timezone-aware.

    Returns:
        datetime: The current UTC datetime as a timezone-aware object.
    """
    return datetime.now(pytz.UTC)

def detect_datetime_format(date_str):
    """
    Determines the datetime format string for decoding a given datetime string.

    Supports detection of formats commonly returned by Vultr and Cloudflare APIs:
    - ISO 8601 with 'Z' suffix for UTC (e.g., '2023-06-01T12:34:56.789Z')
    - ISO 8601 with timezone offset (e.g., '2023-06-01T12:34:56+00:00')

    Args:
        date_str (str): The datetime string to analyze.

    Returns:
        str: The corresponding datetime format string for use with datetime.strptime.

    Raises:
        ValueError: If the datetime format is unknown or unsupported.
    """
    if date_str.endswith('Z'):
        fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    elif '+' in date_str or '-' in date_str[19:]:
        fmt = "%Y-%m-%dT%H:%M:%S%z"
    else:
        raise ValueError("Unknown datetime format")
    return fmt

def print_yes_no(prompt):
    while True:
        try:
            response = input(prompt + " (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'.")
        except KeyboardInterrupt:
            print("\nExiting.")
            exit()

def print_text_prompt(prompt):
    while True:
        try:
            response = input(prompt)
            return response
        except KeyboardInterrupt:
            print("\nExiting.")
            exit()

def print_input_menu(options, prompt, value_key, display_key, none_option = False, headers = None):
    """
    Displays a menu of selectable options to the user, prompts for a selection, and returns the user's choice along with the list of options.
    Args:
        options (list): A list of dictionaries representing the selectable options.
        prompt (str): The prompt message to display to the user.
        value_key (str): The key in each option dictionary whose value will be used as the option's identifier.
        display_key (list): A list of keys whose values will be displayed for each option.
        none_option (bool, optional): If True, includes a 'None' option allowing the user to clear their selection. Defaults to False.
    Returns:
        tuple: A tuple containing:
            - option (str): The user's selected option.
            - out_list (list): The list of options displayed, including any 'None' option if specified.
    Raises:
        KeyboardInterrupt: If the user interrupts input (e.g., with Ctrl+C), prints an exit message and terminates the program.
    """
    out_list = []
    print_list = []
    inst_count = 1
    base_value = 1

    if none_option:
        base_value = 0
        out_list.append(['', 'None'])

    while True:
        for i in options:
            if inst_count == 1 and none_option: # If an option of 'None' should be included, add it here.
                print_list.append(['0', 'None (Clear Selection)'])
            out_list.append([i[value_key], i[display_key[0]]])
            print_row = []
            print_row.append(str(inst_count))
            for j in display_key: # Add elements of display columns to row.
                print_row.append(i[j])
            print_list.append(print_row)
            inst_count += 1

        if headers is None:
            print(tabulate(print_list)) # Print menu output
        else:
            print(tabulate(print_list, headers = headers))

        if settings.PRINT_TIMESTAMP:
            print(f"{utc_to_local(get_utc_now())}")
        try:
            option = input(prompt)
            if not valid_option(option, out_list, base_value):
                print_list = []
                inst_count = 1
                continue
        except KeyboardInterrupt:
            print("\nExiting.")
            exit()
        return option, out_list

def print_output_table(data, headers=None):
    """
    Prints a formatted table to the console using the provided data and headers.

    Args:
        data (list of dict): The data to be displayed in the table, where each dictionary represents a row.
        headers (list of str, optional): The headers for the table columns. If None, keys from the first row are used.

    Returns:
        None
    """
    if not data:
        print("No data to display.")
        return

    if headers is None:
        # headers = list(data[0].keys())
        print(tabulate(data))
    else:
        # table_data = [[row.get(header, '') for header in headers] for row in data]
        # print(tabulate(table_data, headers=headers, tablefmt='grid'))
        print(tabulate(data, headers=headers))

def valid_option(option, options, base_value):
    """
    Validates if the provided option is a valid selection from a list of options, considering a base value offset.
    Args:
        option (str or int): The user's selected option, expected to be convertible to an integer.
        options (list): The list of available options to select from.
        base_value (int): The starting index or offset for valid options.
    Returns:
        bool: True if the option is a valid selection within the allowed range; False otherwise.
    Side Effects:
        Prints messages to stdout for invalid selections, out-of-range selections, or options marked as "coming soon".
    Notes:
        - If `option` is not an integer, prints "Invalid Selection." and returns False.
        - If `option` is 98 or 99, prints "Option Coming Soon".
        - If `option` is outside the valid range, prints a warning and returns False.
    """
    if base_value < 0:
        base_value = 0

    options_len = len(options) - 1 + base_value

    try:
        i_option = int(option)
    except ValueError:
        print(f"Invalid Selection.")
        return False

    match i_option:
        case 99:
            print('Option Coming Soon')
        case 98:
            print('Option Coming Soon')

    if not base_value <= i_option <= options_len:
        print('Selection is out of range. Select valid option.')
        return False

    return True

def valid_response_vultr(output):
    """
    Checks the response from the Vultr API for errors and prints error details if present.

    Args:
        output (dict): The response body from the Vultr API.

    Returns:
        bool: False if an error is present in the response and prints the error details;
              True otherwise.
    """
    if output.get('error'):
        print(f' {output['error_detail']['status']}: {output['error_detail']['error']}')
        return False
    else:
        return True

def valid_response_cloudflare(output):
    """
    Checks the response from the Cloudflare API for errors and prints error details if present.

    Args:
        output (dict): The response body from the Cloudflare API.

    Returns:
        bool: False if an error is present in the response, True otherwise.

    Side Effects:
        Prints error messages to the console if errors are found in the response.
    """
    if output.get('error'):
        print(f'Error: {output['error']} - Success: {output['error_detail']['success']}')
        for e in output['error_detail']['errors']:
            print(f"  Code : {e['code']} - Message : {e['message']}")
        return False
    else:
        return True

def ip6_network_prefix(ip6_address):
    """
    Given an IPv6 address (with optional prefix), return the corresponding IPv6 network.

    Args:
        ip6_address (str): An IPv6 address, optionally with a prefix (e.g., '2001:db8::1/64').

    Returns:
        ipaddress.IPv6Network: The IPv6 network corresponding to the given address and prefix.

    Raises:
        ValueError: If the provided address is not a valid IPv6 address.

    Example:
        >>> ip6_network_prefix('2001:db8::1/64')
        IPv6Network('2001:db8::/64')
    """
    ipv6_interface = ipaddress.IPv6Interface(ip6_address)
    return ipv6_interface.network

def format_bytes(size_in_bytes):
    """
    Converts a size in bytes to a human-readable string with appropriate units.
    Args:
        size_in_bytes (int or float): The size in bytes to format.
    Returns:
        str: The formatted size string with units (e.g., '1.23 MB', '456.00 bytes').
    Examples:
        >>> format_bytes(1024)
        '1.00 KB'
        >>> format_bytes(1048576)
        '1.00 MB'
        >>> format_bytes(500)
        '500.00 bytes'
    """
    units = ["bytes", "KB", "MB", "GB", "TB", "PB"]  # Define the units
    power = 1024
    n = 0

    while size_in_bytes >= power and n < len(units) - 1:
        size_in_bytes /= power
        n += 1

    return f"{size_in_bytes:.2f} {units[n]}"

def format_currency(value_as_number):
    """
    Formats a numeric value as a currency string in US dollars.

    Args:
        value_as_number (int, float, or str): The numeric value to format.

    Returns:
        str: The formatted currency string (e.g., "$ 1,234.56").
        If the input cannot be converted to a float, returns the original input.

    Examples:
        >>> format_currency(1234.56)
        '$ 1,234.56'
        >>> format_currency("1000")
        '$ 1,000.00'
        >>> format_currency("abc")
        'abc'
    """
    try:
        # Convert to float to handle both int and float inputs
        value_as_number = float(value_as_number)
        # Format to 2 decimal places with commas for thousands
        return "$ {:,.2f}".format(value_as_number)
    except (ValueError, TypeError):
        return value_as_number
