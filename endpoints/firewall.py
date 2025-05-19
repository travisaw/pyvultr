from util import utc_to_local, valid_option
from tabulate import tabulate

class Firewall:
    firewall_id = str('')
    firewall_desc = str('')

    def __init__(self, api):
        self.api = api

    def get_firewalls(self):
        url = 'firewalls'
        data = self.api.api_get(url)
        # print(data)
        fw_list = []
        fw_count = 1
        for i in data['firewall_groups']:
            if fw_count == 1:
                print('0. None')
            inst = [i['id'], i['description']]
            fw_list.append(inst)
            print(str(fw_count) + '. '+ i['description'])
            fw_count += 1
        option = input("What firewall to select?: ")
        if not valid_option(option, fw_list):
            print("Invalid Option")
            return
        self.firewall_id = fw_list[int(option) - 1][0]
        self.firewall_desc = fw_list[int(option) - 1][1]

    def get_firewall(self):
        url = 'firewalls/' + self.firewall_id
        data = self.api.api_get(url)
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
        print(data)

    def delete_firewall(self):
        url = 'firewalls/' + self.firewall_id
        data = self.api.api_delete(url)
        print(data)

    def get_firewall_rules(self):
        url = 'firewalls/' + self.firewall_id + '/rules'
        data = self.api.api_get(url)
        result = []
        header = ['Type', 'Action', 'Protocol', 'Ip', 'Notes']
        for i in data['firewall_rules']:
            row = [
                i['type'],
                i['action'],
                i['protocol'],
                i['subnet'] + '/' + str(i['subnet_size']),
                i['notes']
            ]
            result.append(row)
        print(tabulate(result, header))

    def delete_all_firewall_rules(self):
        pass

    def add_ip_to_firewall_rules(self):
        pass