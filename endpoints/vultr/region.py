from util import print_input_menu, valid_response_vultr, print_output_table, utc_str_to_local
from data import create_data_cache, load_data_cache
import settings

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
    preferred_region_ids = settings.PREFERRED_REGION_IDS

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

    def print_region(self):
        if self.region_selected():
            sel_region = next((region for region in self.regions['regions'] if region['id'] == self.region_id), None)
            if sel_region:
                print(sel_region)
                data = [
                    ['ID', sel_region['id']],
                    ['City', sel_region['city']],
                    ['Country', sel_region['country']],
                    ['Continent', sel_region['continent']],
                    ['Options', sel_region['options']],
                ]
                print_output_table(data)

    def get_all_region(self):
        """
        Displays a menu of available regions for selection and updates the instance's region ID and description
        based on the user's choice.

        Utilizes the `print_input_menu` function to present the regions and prompt the user for input.
        The selected region's ID and description are stored in `self.region_id` and `self.region_desc`.

        Returns:
            None
        """
        option, r_list = print_input_menu(self.regions['regions'], 'What region to select?: ', 'id', ['city', 'country', 'continent'], False)
        self.region_id = r_list[int(option) - 1][0]
        self.region_desc = r_list[int(option) - 1][1]

    def get_preferred_region(self):
        """
        Prompts the user to select a preferred region from a list of region IDs.
        Iterates through the preferred region IDs and matches them with available regions.
        Displays a menu for the user to choose a region, showing details such as city, country, and continent.
        Sets the selected region's ID and description as instance attributes.
        Returns:
            None
        """
        regions = []
        for o in self.preferred_region_ids:
            for region in self.regions["regions"]:
                if region.get("id") == o:
                    regions.append(region)
                    break
        option, r_list = print_input_menu(regions, 'What region to select?: ', 'id', ['city', 'country', 'continent'], False)
        self.region_id = r_list[int(option) - 1][0]
        self.region_desc = r_list[int(option) - 1][1]

    def city_from_id(selct, region_id):
        for region in selct.regions['regions']:
            if region['id'] == region_id:
                return region['city']
        return region_id

    def region_selected(self):
        """
        Checks if a region has been selected.

        Returns:
            bool: True if `region_id` is not an empty string, False otherwise.
                  Prints a message if no region is selected.
        """
        if self.region_id != '':
            return True
        else:
            print('No Region Selected!')
            return False
