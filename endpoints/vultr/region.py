from util import print_input_menu, valid_response_vultr

class Region:
    """
    A class to interact with the Vultr Regions API, allowing users to list and select regions.
    Attributes:
        region_id (str): The ID of the selected region.
        region_desc (str): The description of the selected region.
    Methods:
        __init__(api):
            Initializes the Region object with the provided API client.
        get_regions():
            Retrieves all available regions from the Vultr API, displays them to the user,
            and prompts for a selection. Sets the selected region's ID and description.
        get_preferred_region():
            Displays a hardcoded list of preferred regions to the user and prompts for a selection.
            Sets the selected region's ID and description.
    """
    region_id = str('')
    region_desc = str('')

    def __init__(self, api):
        """
        Initialize the Region endpoint with the provided API client.

        Args:
            api: An instance of the API client used to make requests to the Vultr API.
        """
        self.api = api

    def get_regions(self):
        """
        Retrieves a list of available regions from the Vultr API, displays them to the user,
        and prompts for a selection. Sets the selected region's ID and description as instance attributes.

        Returns:
            None

        Side Effects:
            Updates self.region_id and self.region_desc with the selected region's ID and description.

        Raises:
            May raise exceptions if the API response is invalid or if user input is incorrect.
        """
        url = 'regions'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, r_list = print_input_menu(data['regions'], 'What region to select?: ', 'id', ['description'], True)
            self.region_id = r_list[int(option) - 1][0]
            self.region_desc = r_list[int(option) - 1][1]

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
