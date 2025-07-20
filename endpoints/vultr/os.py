from util import print_input_menu, print_output_table, valid_response_vultr
from data import create_data_cache, load_data_cache
# import settings

class OS:

    os_id = str('')
    os_desc = str('')

    def __init__(self, api):
        self.api = api
        self.cache_file = 'vultr_os.json'
        self.oss = self.load_os()

    def load_os(self):
        data = load_data_cache(self.cache_file)
        if data is None:
            print('No cached operating systems found, retrieving from API.')
            self.save_os()
            data = load_data_cache(self.cache_file)
        return data

    def save_os(self):
        url = 'os'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            print('Saving operating system data')
            create_data_cache(self.cache_file, data)
