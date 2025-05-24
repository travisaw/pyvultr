from util import utc_to_local, print_input_menu, valid_response
from tabulate import tabulate

class Zone:
    zone_id = str('')
    zone_detail = {}
    dns_records = {}
    dns_records_header = ['Name', ' Type', 'Content', 'Proxied']
    dns_record_id = str('')
    dns_record = {}

    def __init__(self, api):
        self.api = api

    def verify_token(self):
        url = 'user/tokens/verify'
        data = self.api.api_get(url)
        print(data)

    def get_zones(self):
        url = 'zones'
        data = self.api.api_get(url)
        if valid_response(data):
            option, inst_list = print_input_menu(data['result'], 'What zone to select?: ', 'id', 'name', True)
            self.zone_id = inst_list[int(option) - 1][0]
            self.get_zone()
            self.get_dns_records()

    def get_zone(self):
        url = f'zones/{self.zone_id}'
        data = self.api.api_get(url)
        self.zone_detail = data['result']
        # if valid_response(data):
        #     print(data)

    def print_zone(self):
        result = [
            ['Name: ', self.zone_detail['name']],
            ['Status: ', self.zone_detail['status']],
            ['Paused: ', self.zone_detail['paused']],
            ['Name Servers: ', self.zone_detail['name_servers']],
            ['Original Registrar: ', self.zone_detail['original_registrar']],
            ['Date Created: ', utc_to_local(self.zone_detail['created_on'])],
            ['Date Activated: ', utc_to_local(self.zone_detail['activated_on'])],
            ['Date Updated: ', utc_to_local(self.zone_detail['modified_on'])],
        ]
        print(tabulate(result))

    def get_dns_records(self):
        url = f'zones/{self.zone_id}/dns_records'
        data = self.api.api_get(url)
        self.dns_records = data['result']

    def print_dns_records(self):
        # print(self.dns_records)
        result = []
        for i in self.dns_records:
            row = [
                i['name'],
                i['type'],
                i['content'][:40],
                i['proxied'],
            ]
            result.append(row)
        print(tabulate(result, self.dns_records_header))

    def select_dns_record_of_type(self, type):
        result = []
        for i in self.dns_records:
            if i['type'] == type:
                row = {'id': i['id'], 'name': i['name']}
                result.append(row)
        option, inst_list = print_input_menu(result, 'What entry to select?: ', 'id', 'name', True)
        self.dns_record_id = option
