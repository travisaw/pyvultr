from datetime import datetime
import pytz
import tzlocal

def utc_to_local(utc_string):
    utc_format = "%Y-%m-%dT%H:%M:%S%z"

    # Parse the UTC string into a datetime object
    utc_dt = datetime.strptime(utc_string, utc_format)

    # Get timezone of local system
    timezone = str(tzlocal.get_localzone()) 
    # print(timezone)

    # Localize the UTC datetime object
    # local_tz = pytz.timezone('America/New_York')  # Replace with your desired local timezone
    local_tz = pytz.timezone(timezone)  # Replace with your desired local timezone
    local_dt = utc_dt.astimezone(local_tz)

    # If you need to convert it back to a string in a specific format
    # local_dt_string = local_dt.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    local_dt_string = local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")

    # print(local_dt_string)
    return local_dt_string

def valid_option(option, options):
    try:
        i_option = int(option)
    except ValueError:
        print(f"{option} is not an integer")
        return False

    if not 0 <= i_option < len(options):
        print('Selection is out of range. Select valid option.')
        return False

    return True
