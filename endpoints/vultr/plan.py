from util import print_input_menu, valid_response

class Plan:

    def __init__(self, api):
        self.api = api

    def get_plans(self):
        url = 'plans'
        data = self.api.api_get(url)
        if valid_response(data):
            option, p_list = print_input_menu(data['plans'], 'What plan to select?: ', 'id', 'description', True)
            self.plan_id = p_list[int(option) - 1][0]
            self.plan_desc = p_list[int(option) - 1][1]

    def get_preferred_plan(self):
        return [
            {'id': 'atl', 'name': 'Atlanta'},
            {'id': 'ewr', 'name': 'New York'},
        ]
