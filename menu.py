
from endpoints.vultr.account import get_account_info
from endpoints.vultr.instance import Instance
from endpoints.vultr.firewall import Firewall
from endpoints.vultr.plan import Plan
from endpoints.vultr.region import Region
from endpoints.vultr.snapshot import Snapshot
from endpoints.cloudflare.zone import Zone
from util import print_input_menu

class Menu():
    def __init__(self, vultr_api, cloudflare_api):
        self.vultr_api = vultr_api
        self.cloudflare_api = cloudflare_api
        self.obj_fw = Firewall(self.vultr_api)
        self.obj_p = Plan(self.vultr_api)
        self.obj_r = Region(self.vultr_api)
        self.obj_ss = Snapshot(self.vultr_api)
        self.obj_cf = Zone(self.cloudflare_api)
        self.obj_i = Instance(self.vultr_api, self.obj_fw, self.obj_ss, self.obj_cf, self.obj_p, self.obj_r)

    def main_menu(self):
        options = [
            {'id': 1, 'name': 'Account'},
            {'id': 2, 'name': 'Instances'},
            {'id': 3, 'name': 'Firewall'},
            {'id': 4, 'name': 'Snapshot'},
            {'id': 5, 'name': 'DNS Zones'},
            {'id': 6, 'name': 'Exit'},
        ]
        option, inst_list = print_input_menu(options, 'What area?: ', 'id', 'name', False)
        match option:
            case '1':
                self.account()
            case '2':
                self.instance()
            case '3':
                self.firewall()
            case '4':
                self.snapshot()
            case '5':
                self.dns_zone()
            case '6':
                exit()

    def account(self):
        options = [
            {'id': 1, 'name': 'Show Account Details'},
            {'id': 2, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                get_account_info(self.vultr_api)
                self.account()
            case '2':
                self.main_menu()

    def instance(self):
        options = [
            {'id': 1, 'name': 'Show Instances'},
            {'id': 2, 'name': 'Show Instance'},
            {'id': 3, 'name': 'Create Instance'},
            {'id': 4, 'name': 'Delete Instance'},
            {'id': 5, 'name': 'Create IP4 DNS Name from Hostname'},
            {'id': 6, 'name': 'Create IP6 DNS Name from Hostname'},
            {'id': 7, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_i.get_instances()
                self.instance()
            case '2':
                self.obj_i.print_instance()
                self.instance()
            case '3':
                self.obj_i.create_instance_prompt()
                self.instance()
            case '4':
                self.obj_i.delete_instance()
                self.instance()
            case '5':
                self.obj_i.dns_from_hostname_ip4()
                self.instance()
            case '6':
                self.obj_i.dns_from_hostname_ip6()
                self.instance()
            case '7':
                self.main_menu()

    def firewall(self):
        options = [
            {'id': 1, 'name': 'Show Firewalls'},
            {'id': 2, 'name': 'Show Selected Firewall'},
            {'id': 3, 'name': 'Create Firewall'},
            {'id': 4, 'name': 'Delete Firewall'},
            {'id': 5, 'name': 'Show Firewall Rules'},
            {'id': 6, 'name': 'Delete All Firewall Rules'},
            {'id': 7, 'name': 'Add Current IP to Firewall Rules'},
            {'id': 8, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_fw.get_firewalls()
                self.firewall()
            case '2':
                self.obj_fw.print_firewall()
                self.firewall()
            case '3':
                self.obj_fw.create_firewall_prompt()
                self.firewall()
            case '4':
                self.obj_fw.delete_firewall()
                self.firewall()
            case '5':
                self.obj_fw.print_firewall_rules()
                self.firewall()
            case '6':
                self.obj_fw.delete_all_firewall_rules()
                self.firewall()
            case '7':
                self.obj_fw.add_ip_to_firewall_rules()
                self.firewall()
            case '8':
                self.main_menu()

    def snapshot(self):
        options = [
            {'id': 1, 'name': 'Show Snapshots'},
            {'id': 2, 'name': 'Show Selected Snapshot'},
            {'id': 3, 'name': 'Create Snapshot'},
            {'id': 4, 'name': 'Delete Snapshot'},
            {'id': 5, 'name': 'Update Snapshot'},
            {'id': 6, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_ss.get_snapshots()
                self.snapshot()
            case '2':
                self.obj_ss.get_snapshot()
                self.snapshot()
            case '3':
                ss_name = input("New snapshot Name?: ")
                self.obj_ss.create_snapshot(ss_name, self.obj_i.instance_id)
                self.snapshot()
            case '4':
                self.obj_ss.delete_snapshot()
                self.snapshot()
            case '5':
                ss_name = input("New snapshot Name?: ")
                self.obj_ss.update_snapshot(ss_name)
                self.snapshot()
            case '6':
                self.main_menu()

    def dns_zone(self):
        options = [
            {'id': 1, 'name': 'Show Zones'},
            {'id': 2, 'name': 'Show Selected Zone'},
            {'id': 3, 'name': 'Show Zone DNS Records'},
            {'id': 4, 'name': 'Select Zone DNS Record'},
            {'id': 5, 'name': 'Show DNS Record Details'},
            {'id': 6, 'name': 'Create DNS Record'},
            {'id': 7, 'name': 'Verify Tokens'},
            {'id': 8, 'name': 'Go Back'},
        ]
        option, inst_list = print_input_menu(options, 'What action?: ', 'id', 'name', False)
        match option:
            case '1':
                self.obj_z.get_zones()
                self.dns_zone()
            case '2':
                self.obj_z.print_zone()
                self.dns_zone()
            case '3':
                self.obj_z.print_dns_records()
                self.dns_zone()
            case '4':
                self.obj_z.get_dns_record_of_type('')
                self.dns_zone()
            case '5':
                self.obj_z.print_dns_record()
                self.dns_zone()
            case '6':
                self.obj_z.create_dns_record()
                self.dns_zone()
            case '7':
                self.obj_z.verify_token()
                self.dns_zone()
            case '8':
                self.main_menu()
