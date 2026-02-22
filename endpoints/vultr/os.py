from util import print_input_menu, print_output_table, valid_response_vultr, yellow_text
from data import create_data_cache, load_data_cache
import settings

class OS:
    """
    The OS class provides methods for managing and selecting operating systems using the Vultr API.
        os_id (str): The ID of the currently selected operating system.
        os_desc (str): The description (name) of the currently selected operating system.
        preferred_os_ids (list): List of preferred OS IDs, typically loaded from settings.
        os (dict or list): The loaded operating system data.
    Methods:
        __init__(self, api):
            Initializes the OS class with the provided API client, sets up caching, and loads OS data.
        load_os(self):
            Loads operating system data from the cache file. If the cache is missing or empty,
            retrieves data from the API and caches it.
        save_os(self):
            Retrieves the list of operating systems from the Vultr API and saves it to the cache file.
        print_os(self):
            Prints information about the currently selected operating system, including its ID, name,
        get_all_os(self):
            Displays a menu of all available operating systems for user selection, and sets the selected OS.
        get_preferred_os(self):
            Displays a menu of preferred operating systems for user selection, and sets the selected OS.
        __os_selected(self):
            Checks if an operating system has been selected and prints a message if not.
    """
    os_id = str('')
    os_desc = str('')
    preferred_os_ids = settings.PREFERRED_OS_IDS

    def __init__(self, api):
        """
        Initializes the class with the provided API object, sets the cache file name,
        and loads the operating system data from the cache or source.

        Args:
            api: The API client instance used for making requests.

        Attributes:
            api: Stores the provided API client instance.
            cache_file (str): The filename used for caching OS data.
            os: The loaded operating system data.
        """
        self.api = api
        self.cache_file = 'vultr_os.json'
        self.os = self.load_os()

    def load_os(self):
        """
        Loads the operating system data from the cache file.

        If the cache does not exist or is empty, retrieves the data from the API,
        saves it to the cache, and then loads it again.

        Returns:
            dict or list: The cached operating system data, or the data retrieved from the API if not cached.
        """
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached operating systems found, retrieving from API.')
            self.save_os()
            data = load_data_cache(self.cache_file)
        return data

    def save_os(self):
        """
        Retrieves operating system data from the Vultr API, saves it to a cache file,
        and reloads the operating system data.
        The method performs the following steps:
        1. Sends a GET request to the 'os' endpoint using the API client.
        2. Validates the response using `valid_response_vultr`.
        3. If the response is valid, saves the data to a cache file and reloads the OS data.
        Returns:
            None
        """
        url = 'os'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving operating system data')
            create_data_cache(self.cache_file, data)
            self.load_os()

    def print_os(self):
        """
        Prints information about the currently selected operating system.

        If an OS is selected, this method retrieves its details from the internal OS list
        and prints both the raw OS dictionary and a formatted table containing its ID, name,
        architecture, and family.

        Returns:
            None
        """
        if self.__os_selected():
            sel_os = next((os for os in self.os['os'] if os['id'] == self.os_id), None)
            if sel_os:
                data = [
                    ['ID', sel_os['id']],
                    ['Name', sel_os['name']],
                    ['Architecture', sel_os['arch']],
                    ['Family', sel_os['family']],
                ]
                print_output_table(data)

    def get_all_os(self):
        """
        Displays a menu of available operating systems for selection, prompts the user to choose one,
        and sets the selected OS's ID and description as instance attributes.

        The menu displays OS options with their ID, name, architecture, and family.
        The user's selection determines which OS is chosen.

        Side Effects:
            Sets self.os_id to the ID of the selected OS.
            Sets self.os_desc to the description (name) of the selected OS.
        """
        option, r_list = print_input_menu(self.os['os'], 'What OS to select?: ', 'id', ['id', 'name', 'arch', 'family'], False)
        self.os_id = r_list[int(option) - 1][0]
        self.os_desc = r_list[int(option) - 1][1]

    def get_preferred_os(self):
        """
        Presents a menu of preferred operating systems to the user and allows selection.

        Iterates through the list of preferred OS IDs, matches them with available OS entries,
        and displays a selection menu. Updates the instance's `os_id` and `os_desc` attributes
        based on the user's choice.

        Returns:
            None
        """
        os_out = []
        for o in self.preferred_os_ids:
            for os in self.os['os']:
                if os.get('id') == o:
                    os_out.append(os)
                    break
        option, r_list = print_input_menu(os_out, 'What OS to select?: ', 'id', ['id', 'name', 'arch', 'family'], False)
        self.os_id = r_list[int(option) - 1][0]
        self.os_desc = r_list[int(option) - 1][1]

    def __os_selected(self):
        """
        Checks if an operating system (OS) has been selected.

        Returns:
            bool: True if an OS has been selected (i.e., self.os_id is not an empty string),
            False otherwise. Prints a message if no OS is selected.
        """
        if self.os_id != '':
            return True
        else:
            print(yellow_text('No OS Selected!'))
            return False

