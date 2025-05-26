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
        result = [
            ['Status: ', data['result']['status']],
            ['Success: ', data['success']],
            ['Errors: ', data['errors']],
            ['Message: ', data['messages'][0]['message']],
            ['Message Code: ', data['messages'][0]['code']],
        ]
        print(tabulate(result))

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
        if valid_response(data):
            self.zone_detail = data['result']

    def print_zone(self):
        if 'name' in self.zone_detail:
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
        else:
            print("NO ZONE SELECTED!")

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

    def get_dns_record_of_type(self, type):
        result = []
        for i in self.dns_records:
            if i['type'] == type or type == '':
                row = {'id': i['id'], 'name': i['name']}
                result.append(row)
        option, dns_list = print_input_menu(result, 'What entry to select?: ', 'id', 'name', True)
        self.dns_record_id = dns_list[int(option) - 1][0]

    def print_dns_record(self):
        match = next((d for d in self.dns_records if d.get('id') == self.dns_record_id), None)
        result = [
            ['Name: ', match['name']],
            ['Type: ', match['type']],
            ['Content: ', match['content']],
            ['Proxiable: ', match['proxiable']],
            ['Proxied: ', match['proxied']],
            ['TTL: ', match['ttl']],
            ['Settings: ', match['settings']],
            ['Meta: ', match['meta']],
            ['Comment: ', match['comment']],
            ['Tags: ', match['tags']],
            ['Created On: ', utc_to_local(match['created_on'])],
            ['Modified On: ', utc_to_local(match['modified_on'])],
        ]
        print(tabulate(result))

    def create_dns_record_prompt(self):
        name = input('DNS Name:')
        content = input('IP Address:')
        body = {
            "comment": "Added by pyvultr",
            "content": content,
            "name": name,
            "proxied": True,
            "ttl": 3600,
            "type": "A"
        }
        self.create_dns_record(body)

    def create_dns_record(self, body):
        url = f'zones/{self.zone_id}/dns_records'
        data = self.api.api_post(url, body)
        print(data)
        if valid_response(data):
            print('DNS entry created and selected')
            # self.dns_record_id = data['instance']['id']
            # self.get_instance()

    def delete_instance(self):
        # if 'prod' in self.instance_tags:
        #     print(f"CANNOT DELETE PRODUCTION INSTANCE")
        #     return
        url = f'zones/{self.zone_id}/dns_records/{self.dns_record_id}'
        data = self.api.api_delete(url)
        if valid_response(data):
            print(f" {data['status']}: {data['info']}")
