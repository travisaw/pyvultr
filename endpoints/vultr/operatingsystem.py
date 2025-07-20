from util import print_input_menu, print_output_table, valid_response_vultr
from data import create_data_cache, load_data_cache
# import settings

class OperatingSystem:

    os_id = str('')
    os_desc = str('')

    def __init__(self, api):
        self.api = api
        self.cache_file = 'vultr_operatingsystems.json'
        self.oss = self.load_operatingsystems()

    def load_operatingsystems(self):
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached regions found, retrieving from API.')
            self.save_operatingsystems()
            data = load_data_cache(self.cache_file)
        return data

    def save_operatingsystems(self):
        url = 'os'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving operating system data')
            create_data_cache(self.cache_file, data)
