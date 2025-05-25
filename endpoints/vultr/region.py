from util import print_input_menu, valid_response

class Region:
    region_id = str('')
    region_desc = str('')

    def __init__(self, api):
        self.api = api

    def get_regions(self):
        url = 'regions'
        data = self.api.api_get(url)
        if valid_response(data):
            option, r_list = print_input_menu(data['regions'], 'What region to select?: ', 'id', 'description', True)
            self.region_id = r_list[int(option) - 1][0]
            self.region_desc = r_list[int(option) - 1][1]

    def get_preferred_region(self):
        options = [
            {'id': 'atl', 'name': 'Atlanta'},
            {'id': 'ewr', 'name': 'New York'},
        ]
        option, r_list = print_input_menu(options, 'What region to select?: ', 'id', 'name', False)
        self.region_id = r_list[int(option) - 1][0]
        self.region_desc = r_list[int(option) - 1][1]
