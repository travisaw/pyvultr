from util import print_input_menu, valid_response_vultr

class Region:
    """Contains methods for interacting with the Vultr Regions API."""
    region_id = str('')
    region_desc = str('')

    def __init__(self, api):
        self.api = api

    def get_regions(self):
        """List all regions and prompt user to select one."""
        url = 'regions'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, r_list = print_input_menu(data['regions'], 'What region to select?: ', 'id', 'description', True)
            self.region_id = r_list[int(option) - 1][0]
            self.region_desc = r_list[int(option) - 1][1]

    def get_preferred_region(self):
        """List 'preferred' regions and prompt user to select one. List hardcoded."""
        options = [
            {'id': 'atl', 'name': 'Atlanta'},
            {'id': 'ewr', 'name': 'New York'},
            {'id': 'ord', 'name': 'Chicago'},
            {'id': 'dfw', 'name': 'Dallas'},
            {'id': 'sjc', 'name': 'San Francisco'},
            {'id': 'lhr', 'name': 'London'},
            {'id': 'ams', 'name': 'Amsterdam'},
        ]
        option, r_list = print_input_menu(options, 'What region to select?: ', 'id', 'name', False)
        self.region_id = r_list[int(option) - 1][0]
        self.region_desc = r_list[int(option) - 1][1]
