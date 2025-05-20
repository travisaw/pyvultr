from util import utc_to_local, print_input_menu, valid_output
from tabulate import tabulate

class Instance:
    instance_id = str('')

    def __init__(self, api):
        self.api = api
            
    def get_instances(self):
        url = 'instances'
        data = self.api.api_get(url)
        option, inst_list = print_input_menu(data['instances'], 'What instance to select?: ', 'id', 'label', True)
        self.instance_id = inst_list[int(option) - 1][0]

    def get_instance(self):
        url = f'instances/{self.instance_id}'
        data = self.api.api_get(url)
        if valid_output(data):
            print(tabulate([
                # ['id', data['instance']['id']],
                ['os', data['instance']['os']],
                ['ram', data['instance']['ram']],
                ['disk', data['instance']['disk']],
                ['main_ip', data['instance']['main_ip']],
                ['vcpu_count', data['instance']['vcpu_count']],
                ['region', data['instance']['region']],
                ['plan', data['instance']['plan']],
                ['date_created', utc_to_local(data['instance']['date_created'])],
                ['status', data['instance']['status']],
                ['allowed_bandwidth', data['instance']['allowed_bandwidth']],
                # ['netmask_v4', data['instance']['netmask_v4']],
                # ['gateway_v4', data['instance']['gateway_v4']],
                ['power_status', data['instance']['power_status']],
                ['server_status', data['instance']['server_status']],
                # ['v6_network', data['instance']['v6_network']],
                ['v6_main_ip', data['instance']['v6_main_ip']],
                # ['v6_network_size', data['instance']['v6_network_size']],
                ['label', data['instance']['label']],
                # ['internal_ip', data['instance']['internal_ip']],
                # ['hostname', data['instance']['hostname']],
                ['tag', data['instance']['tag']],
                ['tags', data['instance']['tags']],
                ['os_id', data['instance']['os_id']],
                ['app_id', data['instance']['app_id']],
                # ['image_id', data['instance']['image_id']],
                ['firewall_group_id', data['instance']['firewall_group_id']],
                ['features', data['instance']['features']],
                ['user_scheme', data['instance']['user_scheme']],
                ['pending_charges', data['instance']['pending_charges']],
            ]))


