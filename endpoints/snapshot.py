from util import utc_to_local, print_input_menu, valid_response, format_bytes
from tabulate import tabulate
from requests import get

class Snapshot:
    snapshot_id = str('')
    snapshot_desc = str('')

    def __init__(self, api):
        self.api = api

    def get_snapshots(self):
        url = 'snapshots'
        data = self.api.api_get(url)
        if valid_response(data):
            option, ss_list = print_input_menu(data['snapshots'], 'What snapshot to select?: ', 'id', 'description', True)
            self.snapshot_id = ss_list[int(option) - 1][0]
            self.snapshot_desc = ss_list[int(option) - 1][1]

    def get_snapshot(self):
        url = f'snapshots/{self.snapshot_id}'
        data = self.api.api_get(url)
        if valid_response(data):
            print(tabulate([
                # ['id', data['snapshot']['id']],
                ['date_created', utc_to_local(data['snapshot']['date_created'])],
                ['description', data['snapshot']['description']],
                ['size', format_bytes(data['snapshot']['size'])],
                ['compressed_size', format_bytes(data['snapshot']['compressed_size'])],
                ['status', data['snapshot']['status']],
            ]))

    def create_snapshot(self):
        pass
    def delete_snapshot(self):
        pass
    def update_snapshot(self):
        pass
