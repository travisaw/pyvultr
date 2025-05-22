from util import utc_to_local, print_input_menu, valid_response, format_bytes
from tabulate import tabulate
from colorama import Fore, Style
from colorama import init as colorama_init

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
                ['status', self.__snapshot_status_color(data['snapshot']['status'])],
            ]))

    def create_snapshot(self, ss_name, instance_id):
        url = 'snapshots'
        body = {
            "instance_id": instance_id,
            "description": ss_name,
        }
        data = self.api.api_post(url, body)
        if valid_response(data):
            print(f" Created snapshot '{data['snapshot']['description']}'")

    def delete_snapshot(self):
        url = f'snapshots/{self.snapshot_id}'
        data = self.api.api_delete(url)
        if valid_response(data):
            print(f" {data['status']}: {data['info']}")
    
    def update_snapshot(self, ss_name):
        url = f'snapshots/{self.snapshot_id}'
        body = {
            "description": ss_name,
        }
        data = self.api.api_put(url, body)
        if valid_response(data):
            print(f" {data['status']}: {data['info']}")

    def __snapshot_status_color(self, status):
        match status:
            case 'pending':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}' 
            case 'complete':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}' 
            case 'deleted':
                return f'{Fore.RED}{status}{Style.RESET_ALL}' 
            case _:
                return status
