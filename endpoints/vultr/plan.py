from util import print_input_menu, valid_response_vultr, print_output_table
from data import create_data_cache, load_data_cache

class Plan:
    """
    Plan class for managing Vultr plans with caching.
    This class provides methods to load, cache, and retrieve plan data from the Vultr API.
    It supports loading plans from a local cache file to minimize API requests and includes
    functionality to save fresh plan data when the cache is missing or outdated. Additionally,
    it offers a method to retrieve a list of preferred plans, which can be customized as needed.
        api: Instance of the API client used for making requests.
        cache_file: Filename for caching plan data locally.
        plans: List of plans loaded from the cache or API.
    Methods:
        __init__(api): Initializes the Plan class with the provided API client.
        load_plans(): Loads plans from the cache file or retrieves them from the API if not cached.
        save_plans(): Retrieves plan data from the Vultr API and saves it to the cache file.
        get_preferred_plan(): Returns a hardcoded list of preferred plans for user selection.
    """

    def __init__(self, api):
        """
        Initializes the Plan class with the provided API client, sets the cache file name, and loads available plans.
            api: An instance of the API client used for making requests.
        Attributes:
            api: Stores the provided API client instance.
            cache_file: The filename used for caching plan data.
            plans: A list of plans loaded from the cache or API.
        """
        self.api = api
        self.cache_file = 'vultr_plans.json'
        self.plans = self.load_plans()

    def load_plans(self):
        """
        Loads plans from the cache file if it exists, otherwise retrieves them from the API.

        Returns:
            A list of plans loaded from the cache or API.
        """
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached plans found, retrieving from API.')
            self.save_plans()
            data = load_data_cache(self.cache_file)
        return data

    def save_plans(self):
        """
        Retrieves plan data from the Vultr API and saves it to a cache file.
        This method sends a GET request to the 'plans' endpoint using the API client.
        If the response is valid, it prints a message and caches the data locally.
        Returns:
            None
        """
        url = 'plans'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving plans data')
            create_data_cache(self.cache_file, data)

    def print_all_plans(self):
        """
        Prints all available plans in a formatted table.
        This method retrieves the plans from the cache and displays them using a table format.
        Returns:
            None
        """
        print_output_table(self.plans['plans'], headers=['id', 'ram', 'disk', 'vcpu_count', 'bandwidth', 'monthly_cost', 'type'])

    def get_preferred_plan(self):
        """
        Returns a list of preferred plans.
        This method provides a hardcoded list of 'preferred' plans for the user to select from.
        Currently, the list is empty and should be populated with plan identifiers or objects
        that represent the preferred options.
        Returns:
            list: A list of preferred plan identifiers or objects.
        """
        """List 'preferred' plans and prompt user to select one. List hardcoded."""
        return [

        ]
