from util import print_input_menu, valid_response_vultr, print_output_table
from data import create_data_cache, load_data_cache

class Region:
    """
    Represents a Vultr region and provides methods to manage region data.
    Attributes:
        region_id (str): The ID of the selected region.
        region_desc (str): The description/name of the selected region.
        api: An API client instance used to interact with Vultr endpoints.
        cache_file (str): The filename for caching region data.
        regions: Cached region data loaded from file.
    Methods:
        __init__(api):
            Initializes the Region instance with the provided API client, sets up the cache file, and loads region data.
        load_regions():
            Loads region data from the cache file. If no cached data is found, retrieves data from the API and caches it.
        save_regions():
            Retrieves region data from the Vultr API and saves it to the cache file if the response is valid.
        get_preferred_region():
            Prompts the user to select a preferred region from a hardcoded list, and sets the region_id and region_desc attributes accordingly.
    """
    region_id = str('')
    region_desc = str('')

    def __init__(self, api):
        """
        Initializes a Region instance.

        Args:
            api: The API client used to interact with the Vultr service.

        Attributes:
            api: Stores the provided API client.
            cache_file (str): The filename for caching region data.
            regions: The loaded region data from the cache file.
        """
        self.api = api
        self.cache_file = 'vultr_regions.json'
        self.regions = self.load_regions()

    def load_regions(self):
        """
        Loads region data from the cache file. If no cached data is found, retrieves region data from the API,
        saves it to the cache, and then loads it from the cache.

        Returns:
            dict or None: The cached region data if available, otherwise None.
        """
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached regions found, retrieving from API.')
            self.save_regions()
            data = load_data_cache(self.cache_file)
        return data

    def save_regions(self):
        """
        Retrieves region data from the Vultr API and saves it to a cache file.

        This method sends a GET request to the 'regions' endpoint using the API client.
        If the response is valid, it prints a message and caches the region data.

        Returns:
            None
        """
        url = 'regions'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving regions data')
            create_data_cache(self.cache_file, data)

    def print_all_regions(self):
        print_output_table(self.regions['regions'], headers=['id', 'city', 'country', 'continent'])

    def print_preferred_regions(self):
        options = ['atl','ewr','ord','dfw','sjc','lhr','ams',]
        for o in options:
            for region in self.regions["regions"]:
                if region.get("id") == o:
                    print(f'{o} - {region["city"]}, {region["country"]}')
                    break
            else:
                print(f'{o} - Airport code not found')

    def get_preferred_region(self):
        """
        Prompts the user to select a preferred region from a hardcoded list of options.

        The method displays a menu of region names and waits for user input to select one.
        Upon selection, it sets the `region_id` and `region_desc` attributes of the instance
        to the corresponding region's ID and name.

        Returns:
            None
        """
        options = [
            {'id': 'atl', 'name': 'Atlanta'},
            {'id': 'ewr', 'name': 'New York'},
            {'id': 'ord', 'name': 'Chicago'},
            {'id': 'dfw', 'name': 'Dallas'},
            {'id': 'sjc', 'name': 'San Francisco'},
            {'id': 'lhr', 'name': 'London'},
            {'id': 'ams', 'name': 'Amsterdam'},
        ]
        option, r_list = print_input_menu(options, 'What region to select?: ', 'id', ['name'], False)
        self.region_id = r_list[int(option) - 1][0]
        self.region_desc = r_list[int(option) - 1][1]

