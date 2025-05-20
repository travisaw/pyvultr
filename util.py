from datetime import datetime
import pytz
import tzlocal
import ipaddress

def utc_to_local(utc_string):
    """Format given UTC time from API into local (US) format"""
    utc_format = "%Y-%m-%dT%H:%M:%S%z"

    # Parse the UTC string into a datetime object
    utc_dt = datetime.strptime(utc_string, utc_format)

    # Get timezone of local system
    timezone = str(tzlocal.get_localzone()) # IE: America/New_York
    # print(timezone)

    # Localize the UTC datetime object
    local_tz = pytz.timezone(timezone)  # Replace with your desired local timezone
    local_dt = utc_dt.astimezone(local_tz)

    # Convert back to a string in a specific format
    local_dt_string = local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    return local_dt_string

def print_input_menu(options, prompt, value_key, display_key, none_option = False):
    """Given a list of options, the options will be printed and the user will be prompted to enter a selection. Both the selection and list are returned."""
    base_value = 1
    if none_option:
        base_value = 0

    while True:
        out_list = []
        inst_count = 1
        for i in options:
            if inst_count == 1 and none_option:
                print('0. None (Return)')
            out_row = [i[value_key], i[display_key]]
            out_list.append(out_row)
            print(str(inst_count) + '. '+ i[display_key])
            inst_count += 1
        try:
            option = input(prompt)
            if not valid_option(option, out_list, base_value):
                continue
        except KeyboardInterrupt:
            print("\nExiting.")
            exit()
        return option, out_list

def valid_option(option, options, base_value):
    """Given the users' input and a list of input options, determine if selected value is valid."""
    try:
        i_option = int(option)
    except ValueError:
        print(f"Invalid Selection.")
        return False

    if not base_value <= i_option <= len(options):
        print('Selection is out of range. Select valid option.')
        return False

    return True

def valid_output(output):
    if output.get('error'):
        print(f'Error {output['error_detail']['status']}: {output['error_detail']['error']}')
        return False
    else:
        return True

def ip6_network_prefix(ip6_address):
    ipv6_interface = ipaddress.IPv6Interface(ip6_address)
    return ipv6_interface.network
