from util import print_input_menu, valid_response

class Zone:

    def __init__(self, api):
        self.api = api

    def verify_token(self):
        url = 'user/tokens/verify'
        data = self.api.api_get(url)
        print(data)

    def get_zones(self):
        url = 'zones'
        data = self.api.api_get(url)
        print(data)
        # if valid_response(data):
        #     option, inst_list = print_input_menu(data['instances'], 'What instance to select?: ', 'id', 'label', True)
        #     self.instance_id = inst_list[int(option) - 1][0]
        #     self.get_instance()
