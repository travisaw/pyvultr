from util import utc_to_local, print_input_menu, valid_response_vultr
from tabulate import tabulate
from colorama import Fore, Style
from colorama import init as colorama_init

class Instance:
    instance_id = str('')
    instance_tags = []
    instance_hostname = ''
    instance_ip4 = ''
    instance_ip6 = ''

    def __init__(self, api, fw_obj, ss_obj, cf_obj, p_obj, r_obj):
        self.api = api
        self.fw_obj = fw_obj
        self.ss_obj = ss_obj
        self.cf_obj = cf_obj
        self.p_obj = p_obj
        self.r_obj = r_obj
        colorama_init(autoreset=True)

    def get_instances(self):
        url = 'instances'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            option, inst_list = print_input_menu(data['instances'], 'What instance to select?: ', 'id', ['label'], True)
            self.instance_id = inst_list[int(option) - 1][0]
            self.get_instance()

    def get_instance(self):
        url = f'instances/{self.instance_id}'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            self.instance_tags = data['instance']['tags']
            self.instance_hostname = data['instance']['hostname']
            self.instance_ip4 = data['instance']['main_ip']
            self.instance_ip6 = data['instance']['v6_main_ip']

    def print_instance(self):
        url = f'instances/{self.instance_id}'
        data = self.api.api_get(url)
        if valid_response_vultr(data):
            self.fw_obj.firewall_id = data['instance']['firewall_group_id']
            self.fw_obj.get_firewall()
            print(tabulate([
                ['Label', data['instance']['label']],
                ['Hostname', data['instance']['hostname']],
                ['Tags', data['instance']['tags']],
                ['Region', data['instance']['region']],
                ['Date Created', utc_to_local(data['instance']['date_created'])],
                ['Plan', data['instance']['plan']],
                ['OS', data['instance']['os']],
                ['OS ID', data['instance']['os_id']],
                ['App Id', data['instance']['app_id']],
                ['vCPU Count', data['instance']['vcpu_count']],
                ['Ram', data['instance']['ram']],
                ['Disk', data['instance']['disk']],
                ['Allowed Bandwidth', data['instance']['allowed_bandwidth']],
                # ['internal_ip', data['instance']['internal_ip']],
                # ['netmask_v4', data['instance']['netmask_v4']],
                ['v4 Main IP', data['instance']['main_ip']],
                # ['gateway_v4', data['instance']['gateway_v4']],
                # ['v6_network', data['instance']['v6_network']],
                ['v6 Main IP', data['instance']['v6_main_ip']],
                # ['v6_network_size', data['instance']['v6_network_size']],
                ['Firewall Group', self.fw_obj.firewall_desc],
                ['Status', self.__instance_status_color(data['instance']['status'])],
                ['Power Status', self.__instance_power_status_color(data['instance']['power_status'])],
                ['Server Status', self.__instance_server_status_color(data['instance']['server_status'])],
                # ['image_id', data['instance']['image_id']],
                ['Features', data['instance']['features']],
                ['User Scheme', data['instance']['user_scheme']],
                ['Pending Charges', data['instance']['pending_charges']],
            ]))

    def create_instance_prompt(self):
        label = input('Hostname/Label?:')
        self.r_obj.get_preferred_region()
        tags = ['pyvultr']
        self.fw_obj.get_firewalls()
        self.ss_obj.get_snapshots()
        body = {
            "region": self.r_obj.region_id,
            "plan": "vc2-1c-1gb",
            "label": label,
            "hostname": label,
            "tags": tags,
            "firewall_group_id": self.fw_obj.firewall_id,
            "snapshot_id": self.ss_obj.snapshot_id,
            "enable_private_network": "false",
            "enable_ipv6": "false",
        }
        self.create_instance(body)

    def create_instance(self, body):
        url = 'instances'
        data = self.api.api_post(url, body)
        if valid_response_vultr(data):
            print('Instance created and selected')
            self.instance_id = data['instance']['id']
            self.get_instance()

    def delete_instance(self):
        if 'prod' in self.instance_tags:
            print(f"CANNOT DELETE PRODUCTION INSTANCE")
            return
        url = f'instances/{self.instance_id}'
        data = self.api.api_delete(url)
        if valid_response_vultr(data):
            print(f" {data['status']}: {data['info']}")

    def dns_from_hostname_ip4(self):
        self.cf_obj.get_zones() # Select DNS zone
        if self.instance_ip4 == '0.0.0.0' or self.instance_ip4 == '':
            return
        body = {
            "comment": "Added by pyvultr",
            "content": self.instance_ip4,
            "name": self.instance_hostname,
            "proxied": False,
            "ttl": 300,
            "type": "A"
        }
        self.cf_obj.create_dns_record(body)

    def dns_from_hostname_ip6(self):
        pass

    def __instance_status_color(self, status):
        match status:
            case 'active':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}'
            case 'pending':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case 'suspended':
                return f'{Fore.RED}{status}{Style.RESET_ALL}'
            case 'resizing':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case _:
                return status

    def __instance_power_status_color(self, status):
        match status:
            case 'running':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}'
            case 'stopped':
                return f'{Fore.RED}{status}{Style.RESET_ALL}'
            case _:
                return status

    def __instance_server_status_color(self, status):
        match status:
            case 'none':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case 'locked':
                return f'{Fore.RED}{status}{Style.RESET_ALL}'
            case 'installingbooting':
                return f'{Fore.YELLOW}{status}{Style.RESET_ALL}'
            case 'ok':
                return f'{Fore.GREEN}{status}{Style.RESET_ALL}'
            case _:
                return status
