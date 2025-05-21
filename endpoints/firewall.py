from util import utc_to_local, print_input_menu, valid_response, ip6_network_prefix
from tabulate import tabulate
from requests import get

class Firewall:
    firewall_id = str('')
    firewall_desc = str('')
    firewall_rules = []
    firewall_rules_header = ['Type', 'Action', 'Protocol', 'Ip', 'Port', 'Notes']

    def __init__(self, api):
        self.api = api

    def get_firewalls(self):
        url = 'firewalls'
        data = self.api.api_get(url)
        if valid_response(data):
            option, fw_list = print_input_menu(data['firewall_groups'], 'What firewall to select?: ', 'id', 'description', True)
            self.firewall_id = fw_list[int(option) - 1][0]
            self.firewall_desc = fw_list[int(option) - 1][1]
            self.get_firewall_rules()

    def get_firewall(self):
        url = f'firewalls/{self.firewall_id}'
        data = self.api.api_get(url)
        if valid_response(data):
            result = [
                ['Description: ', data['firewall_group']['description']],
                ['Date Created: ', utc_to_local(data['firewall_group']['date_created'])],
                ['Date Updated: ', utc_to_local(data['firewall_group']['date_modified'])],
                ['Instance Count: ', data['firewall_group']['instance_count']],
                ['Rule Count: ', data['firewall_group']['rule_count']],
                ['Max Rule Count: ', data['firewall_group']['max_rule_count']]
            ]
            print(tabulate(result))

    def create_firewall(self, description):
        url = 'firewalls'
        body = {'description': description}
        data = self.api.api_post(url, body)
        if valid_response(data):
            print(f" Created firewall '{data['firewall_group']['description']}'")

    def delete_firewall(self):
        url = f'firewalls/{self.firewall_id}'
        data = self.api.api_delete(url)
        if valid_response(data):
            print(f" {data['status']}: {data['info']}")

    def get_firewall_rules(self):
        url = f'firewalls/{self.firewall_id}/rules'
        data = self.api.api_get(url)
        if valid_response(data):
            result = []
            for i in data['firewall_rules']:
                row = [
                    i['id'],
                    i['type'],
                    i['ip_type'],
                    i['action'],
                    i['protocol'],
                    i['port'],
                    i['subnet'],
                    i['subnet_size'],
                    i['source'],
                    i['notes'],
                ]
                result.append(row)
            self.firewall_rules = result

    def print_firewall_rules(self):
        self.get_firewall_rules()
        result = []
        for i in self.firewall_rules:
            row = [
                i[1],
                i[3],
                i[4],
                i[6] + '/' + str(i[7]),
                i[5],
                i[9],
            ]
            result.append(row)
        print(tabulate(result, self.firewall_rules_header))

    def delete_all_firewall_rules(self):
        self.get_firewall_rules()
        for i in self.firewall_rules:
            url = f'firewalls/{self.firewall_id}/rules/{i[0]}'
            data = self.api.api_delete(url)
            if valid_response(data):
                print(f" {data['status']}: {data['info']}")

    def add_ip_to_firewall_rules(self):
        ip4 = get('https://api.ipify.org').content.decode('utf8')
        # ip6 = get('https://api64.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip4))
        # print('My public IP address is: {}'.format(ip6))
        # print('My public IP address is: {}'.format(ip6_network_prefix(ip6)))

        result = []
        params = (
            ('tcp', '1:65535',),
            ('udp', '1:65535',),
            ('icmp', '',),
        )

        url = f'firewalls/{self.firewall_id}/rules'
        for p in params:
            body = {
                    "ip_type": "v4",
                    "protocol": p[0],
                    "port": p[1],
                    "subnet": ip4,
                    "subnet_size": 32,
                    "source": "",
                    "notes": "Example Firewall Rule"
                }
            data = self.api.api_post(url, body)
            if valid_response(data):
                print('Added Firewall Rule')
                detail_row = [
                    data['firewall_rule']['type'],
                    data['firewall_rule']['action'],
                    data['firewall_rule']['protocol'],
                    data['firewall_rule']['subnet'] + '/' + str(data['firewall_rule']['subnet_size']),
                    data['firewall_rule']['port'],
                    data['firewall_rule']['notes'],
                ]
                result.append(detail_row)
        
        print(tabulate(result, self.firewall_rules_header))
        
